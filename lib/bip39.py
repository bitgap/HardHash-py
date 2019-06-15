#!/usr/bin/python3

# This file contains code that generates a BIP39 mnemonic phrase usable for
# Bitcoin Cash or Bitcoin Core HD wallet generation
# This mnemnonic can be used to create a wallet with software such as the
# Bitcoin.com wallet, Blockchain.info, or Electron Cash
#
# Every effort has been made to learn and follow best practices
# in the development of this software. 
# 
# However, this code should be considered academic/experimental
# Use at your own risk
#
# Author: Josh McIntyre
#

import os
import hashlib
import argparse
import sys
import bitstring

WORDS_PATH = os.path.dirname(__file__) + "/bip39_words.txt"
DEF_ENTROPY_BITS = 128

# This function imports the standard BIP39 english word list from file
def read_wordlist():
	with open(WORDS_PATH) as words_file:
		words = [ word.strip() for word in words_file ]

	return words

# This function adds a checksum to the generated entropy
# according to the BIP39 standard
# The standard specifies taking the SHA-256 hash of the
# generated entropy, and then appending the first N/32 bits
# of the hash to the entropy
# This function returns a BitArray of the checksummed data
#
def gen_checksum_entropy(entropy, size_bits):

	# First, take the SHA-256 hash of the generated entropy
	hash = hashlib.sha256(entropy)
	hash_bits = bitstring.BitArray("0x" + hash.hexdigest())

	# Calculate the number of bits for the checksum
	# According to BIP39, checksum bits = entropy bits / 32
	num_checksum_bits = size_bits // 32
	
	# Append the checksum to the entropy
	entropy_bits = bitstring.BitArray("0x" + entropy.hex())
	checksummed_bits = entropy_bits + hash_bits[0:num_checksum_bits]

	return checksummed_bits

# This function maps the entropy to mnemonic words
# According to the BIP39 standard, we will take the
# checksummed entropy and divide it into 11-bit "chunks"
# Each 11-bit number is interpreted as an index from 1-2047,
# mapping to a word from the standard dictionary
#
def map_words(checksummed_entropy, words):

	# Calculate the number of sections to divide the entropy into
	num_chunks = len(checksummed_entropy) // 11

	# Generate the mnemonic word list by mapping each
	# chunk to the appropriate word in the dictionary
	mnemonic = []
	for i in range(0, num_chunks):
		start = i * 11
		end = (i + 1) * 11

		chunk = bitstring.BitArray(checksummed_entropy[start:end])	
		word_index = int(chunk.bin, 2)

		word = words[word_index]
		mnemonic.append(word)

	return mnemonic

# This function provides a simple format for the mnemonic list
def format_mnemonic(mnemonic):

	formatted_mnemonic = ""
	count = 1
	for word in mnemonic:
		formatted_mnemonic += "{} ".format(word)
		count += 1

	return formatted_mnemonic.rstrip()

def get_mnemonic(entropy):

	# Read the word list from file
	words = read_wordlist()

	checksummed_entropy = gen_checksum_entropy(entropy, len(entropy)*8)

	# Generate the mnemonic
	mnemonic = map_words(checksummed_entropy, words)

	# Format and print the result
	return  format_mnemonic(mnemonic)