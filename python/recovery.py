import hashlib
import hmac
from mnemonic import Mnemonic
import ecdsa

def pubkey_to_doge_address(pub_key_bytes: bytes) -> str:

    sha256 = hashlib.sha256(pub_key_bytes).digest()
    ripemd160 = hashlib.new('ripemd160', sha256).digest()
    
    network_byte = b'\x1e' + ripemd160
    

    checksum = hashlib.sha256(hashlib.sha256(network_byte).digest()).digest()[:4]
    binary_address = network_byte + checksum
    
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    value = int.from_bytes(binary_address, 'big')
    result = []
    while value > 0:
        value, mod = divmod(value, 58)
        result.append(alphabet[mod])
    

    pad = 0
    for byte in binary_address:
        if byte == 0: pad += 1
        else: break
            
    return '1' * pad + ''.join(reversed(result))

def derive_bip32_child(parent_key: bytes, parent_chain: bytes, index: int):

    if index >= 0x80000000:
        data = b'\x00' + parent_key + index.to_bytes(4, 'big')
    else:
        sk = ecdsa.SigningKey.from_string(parent_key, curve=ecdsa.SECP256k1)
        vk = sk.verifying_key
        pub = (b'\x02' if vk.to_string()[63] % 2 == 0 else b'\x03') + vk.to_string()[:32]
        data = pub + index.to_bytes(4, 'big')

    I = hmac.new(parent_chain, data, hashlib.sha512).digest()
    IL, IR = I[:32], I[32:]
    ki = (int.from_bytes(IL, 'big') + int.from_bytes(parent_key, 'big')) % ecdsa.SECP256k1.order
    return ki.to_bytes(32, 'big'), IR

def run_fast_offline_check():
    print("Starting Fast Dogecoin Recovery Script\n")
    
    # ⌨️ Get 11 words from the user
    words_input = input("Please enter your 11 words separated by spaces:\n").strip().lower()
    known_words = words_input.split()


    if len(known_words) != 11:
        print("Error: You must enter exactly 11 words!")
        return


    target_address = input("\nPlease enter the target Dogecoin address:\n").strip()

    mnemo = Mnemonic("english")
    wordlist = mnemo.wordlist
    seen_phrases = set()

    print("\n⚡ Scanning 1,536 valid combinations in RAM...")


    paths_to_check = [
        [44 + 0x80000000, 3 + 0x80000000, 0 + 0x80000000, 0],
        [44 + 0x80000000, 0 + 0x80000000, 0 + 0x80000000, 0]
    ]

    for pos in range(12):
        for word in wordlist:

            test_phrase_list = known_words[:pos] + [word] + known_words[pos:]
            test_phrase = " ".join(test_phrase_list)
            

            if mnemo.check(test_phrase) and test_phrase not in seen_phrases:
                seen_phrases.add(test_phrase)
                
                seed_bytes = mnemo.to_seed(test_phrase)
                I = hmac.new(b"Bitcoin seed", seed_bytes, hashlib.sha512).digest()
                master_k, master_c = I[:32], I[32:]
                

                for path in paths_to_check:
                    k, c = master_k, master_c
                    for idx in path:
                        k, c = derive_bip32_child(k, c, idx)
                    
                    for address_index in range(5):
                        child_k, _ = derive_bip32_child(k, c, address_index)
                        sk = ecdsa.SigningKey.from_string(child_k, curve=ecdsa.SECP256k1)
                        vk = sk.verifying_key
                        pub_comp = (b'\x02' if vk.to_string()[63] % 2 == 0 else b'\x03') + vk.to_string()[:32]
                        
                        address = pubkey_to_doge_address(pub_comp)
                        
                        # 🎯 Match found!
                        if address == target_address:
                            print(f"Address found")
                            print(f"Matched Address: {address}")
                            print(f"Your 12-Word Phrase:\n\n{test_phrase}\n")
                            return

    print("\nNo phrase matched this address.")

if __name__ == "__main__":
    run_fast_offline_check()