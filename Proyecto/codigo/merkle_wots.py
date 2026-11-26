"""WOTS y árbol de Merkle con SHA-256 (proyecto TEL252).

Uso: from merkle_wots import H, chain, WOTS, MerkleTree
"""
import hashlib
import math
import os 
import struct
import time

def H(data: bytes) -> bytes:
    """SHA-256"""
    return hashlib.sha256(data).digest()

def chain(X: bytes, steps: int) -> bytes:
    """Aplica H 'steps' veces sobre X de forma iterativa"""
    out = X
    for _ in range(steps):
        out = H(out)
    return out

class WOTS:

    def __init__(self, w=16):
        self.w = w
        self.log_w = int(math.log2(w))
        self.l1 = math.ceil(256 / self.log_w)
        self.max_c = self.l1 * (self.w-1)
        self.l2 = math.floor( math.log2(self.max_c) / self.log_w ) +1
        self.l = self.l1 + self.l2

    def _bytes_to_digits(self, data: bytes, num_digits: int) -> list[int]:
        """Convierte bytes en una lista de dígitos base w"""
        val = int.from_bytes(data, 'big')
        digits = []
        mask = self.w-1
        for _ in range(num_digits):
            digits.append(val & mask)
            val >>= self.log_w
        return digits[::-1] # Big endian digits

    def _get_digits(self, msg_hash: bytes) -> list[int]:
        """Calcula los l1 dígitos del mensaje + l2 dígitos del checksum"""
        d_msg = self._bytes_to_digits(msg_hash, self.l1)
        checksum = sum((self.w-1-d) for d in d_msg)

        c_bytes = checksum.to_bytes(4, 'big')
        c_val = checksum
        d_chk = []
        mask = self.w-1
        for _ in range(self.l2):
            d_chk.append(c_val & mask)
            c_val >>= self.log_w
        d_chk = d_chk[::-1]

        return d_msg + d_chk

    def keygen(self) -> tuple[list[bytes], bytes]:
        """Genera (SK, PK). SK es una lista de l secretos; PK es un hash de 32B"""
        sk = [os.urandom(32) for _ in range(self.l)]
        pk_ends = [chain(sk_i, self.w-1) for sk_i in sk]
        pk_bytes = b''.join(pk_ends)
        pk = H(pk_bytes)
        return sk, pk

    def sign(self, sk: list[bytes], msg: bytes) -> bytes:
        """Firma un mensaje retornando los l elementos concatenados"""
        msg_hash = H(msg)
        digits = self._get_digits(msg_hash)
        sig_blocks = [chain(sk[i], digits[i]) for i in range(self.l)]
        return b''.join(sig_blocks)

    def verify(self, pk: bytes, msg: bytes, sig: bytes) -> bool:
        """Verifica una forma WOTS"""
        if len(sig) != self.l*32:
            return False
        msg_hash = H(msg)
        digits = self._get_digits(msg_hash)

        sig_blocks = [sig[i*32 : (i+1)*32] for i in range(self.l)]
        reconstructed_ends = [
            chain(sig_blocks[i], self.w-1-digits[i]) for i in range(self.l)
        ]
        candidate_pk = H(b''.join(reconstructed_ends))
        return candidate_pk == pk

class MerkleTree:

    def __init__(self, h=4, w=16):
        self.h = h
        self.num_leaves = 1 << h
        self.w = w
        self.wots = WOTS(w=w)
        self.next_index = 0

        self.sk_list = []
        self.pk_list = []
        self.leaves = []

        for _ in range(self.num_leaves):
            sk, pk = self.wots.keygen()
            self.sk_list.append(sk)
            self.pk_list.append(pk)
            self.leaves.append(H(pk)) # La hoja es el hash de la clave pública

        # Construir arbol
        self.tree = [[] for _ in range(self.h+1)]
        self.tree[0] = self.leaves

        for level in range(1, self.h +1):
            prev_level = self.tree[level-1]
            current_level = []
            for i in range(0, len(prev_level), 2):
                parent = H(prev_level[i] + prev_level[i+1])
                current_level.append(parent)
            self.tree[level] = current_level

        self.root = self.tree[self.h][0]

    def get_auth_paths(self, idx: int) -> list[bytes]:
        """Obtiene los h nodos hermanos para el índice idx"""
        auth_path = []
        curr_idx = idx
        for level in range(self.h):
            sibling_idx = curr_idx ^ 1
            auth_path.append(self.tree[level][sibling_idx])
            curr_idx >>= 1
        return auth_path

    def sign(self, msg: bytes) -> bytes:
        """Firma un mensaje usando la clave con estado next_index"""
        if self.next_index >= self.num_leaves:
            raise ValueError("¡ERROR! Claves Merkle agotadas.")

        idx = self.next_index
        self.next_index+=1

        wots_sk = self.sk_list[idx]
        wots_pk = self.pk_list[idx]
        wots_sig = self.wots.sign(wots_sk, msg)
        auth_path = self.get_auth_paths(idx)

        # Estructura de la firma:
        # [4B idx] + [Sig WOTS] + [32B PK_WOTS] + [h*32B AuthPath]
        header = struct.pack('>I', idx)
        auth_bytes = b''.join(auth_path)
        return header + wots_sig + wots_pk + auth_bytes

    @staticmethod
    def verify(root: bytes, msg: bytes, sig: bytes, h=4, w=16) -> bool:
        """Verifica la firma de Merkle"""
        wots = WOTS(w=w)
        expected_sig_len = 4 + (wots.l*32)+32+ (h*32)
        if len(sig) != expected_sig_len:
            return False

        idx = struct.unpack('>I', sig[:4])[0]
        if idx >= (1<<h):
            return False

        offset = 4
        wots_sig_len = wots.l*32
        wots_sig = sig[offset: offset + wots_sig_len]
        offset += wots_sig_len

        wots_pk = sig[offset : offset +32]
        offset += 32

        auth_path = [sig[offset +i*32 : offset + (i+1)*32] for i in range(h)]

        # Verificar firma WOTS
        if not wots.verify(wots_pk, msg, wots_sig):
            return False

        # Reconstruir raiz Merkle
        curr_node = H(wots_pk)
        curr_idx = idx
        for level in range(h):
            sibling = auth_path[level]
            if (curr_idx & 1) == 0:
                curr_node = H(curr_node+sibling)
            else:
                curr_node = H(sibling+curr_node)
            curr_idx >>=1

        return curr_node == root
