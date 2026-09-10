import * as readline from 'readline/promises';
import { stdin as input, stdout as output } from 'process';
import * as bip39 from 'bip39';
import { BIP32Factory } from 'bip32';
import * as ecc from 'tiny-secp256k1';
import * as bitcoin from 'bitcoinjs-lib';

const bip32 = BIP32Factory(ecc);

const DOGECOIN_NETWORK: bitcoin.Network = {
    messagePrefix: '\x19Dogecoin Signed Message:\n',
    bip32: { public: 0x02facafd, private: 0x02fac398 },
    pubKeyHash: 0x1e,
    scriptHash: 0x16,
    wif: 0x9e,
    bech32: ''
};

async function main() {
    console.log("Starting Dogecoin Recovery\n");

    const rl = readline.createInterface({ input, output });

    const wordsInput = await rl.question("Please enter your 11 words separated by spaces:\n");
    const knownWords = wordsInput.trim().toLowerCase().split(' ');

    if (knownWords.length !== 11) {
        console.log("Error: You must enter exactly 11 words!");
        rl.close();
        return;
    }

    const targetAddressInput = await rl.question("\nPlease enter the target Dogecoin address:\n");
    const targetAddress = targetAddressInput.trim();
    
    rl.close();

    console.log("\nScanning 1,536 valid combinations in RAM...");
    
    const wordlist = bip39.wordlists.english;

    for (let pos = 0; pos < 12; pos++) {
        for (const word of wordlist) {
            const testPhraseList = [...knownWords.slice(0, pos), word, ...knownWords.slice(pos)];
            const testPhrase = testPhraseList.join(' ');

            if (bip39.validateMnemonic(testPhrase)) {
                const seed = bip39.mnemonicToSeedSync(testPhrase);
                const root = bip32.fromSeed(seed);

                const paths = ["m/44'/3'/0'/0", "m/44'/0'/0'/0"];

                for (const path of paths) {
                    const accountNode = root.derivePath(path);

                    for (let i = 0; i < 5; i++) {
                        const childNode = accountNode.derive(i);
                        const { address } = bitcoin.payments.p2pkh({
                            pubkey: childNode.publicKey,
                            network: DOGECOIN_NETWORK
                        });

                        if (address === targetAddress) {
                            console.log(`Address found`);
                            console.log(`Matched Address: ${address}`);
                            console.log(`Discovered Path: ${path}/${i}`);
                            console.log(`Your 12-Word Phrase:\n\n${testPhrase}\n`);
                            return; 
                        }
                    }
                }
            }
        }
    }
    console.log("\nNo phrase matched this address.");
}

main().catch(console.error);