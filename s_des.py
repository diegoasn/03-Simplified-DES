#Simplified DES
import fileinput
S0 = [[1,0,3,2], [3,2,1,0], [0,2,1,3], [3,1,3,2]]
S1 = [[0,1,2,3], [2,0,1,3], [3,0,1,0], [2,1,0,3]]

"""permutation(bits, index_list)
   Realiza una permutación/expansión sobre una serie de bits basándose en una lista de
   indices que indica en que posición colocar los elementos.
   bits - Arreglo de bits a permutar/expandir
   index_list - Lista de indices"""
def permutation(bits, index_list):
	per_bits = ''
	for i in index_list:
		per_bits += bits[i]
	return per_bits

"""s_boxes(bits, s_box)
   Realiza la búsqueda de un elemento dentro de la s box utilizando el arreglo de bits
   como indices de la fila y la columna.
   bits - Arreglo de bits
   s_box - Matriz o caja S necesaria en el algoritmo de SDES"""
def s_boxes(bits, s_box):
	row = int(bits[0] + bits[3], 2)
	col = int(bits[1] + bits[2], 2)
	res = bin(s_box[row][col])[2:]
	while len(res) < 2:
		res = '0' + res
	return res

"""xor(a, b)
   Realiza la operación XOR entre dos arreglos de bits.
   a - Arreglo de bits
   b - Arreglo de bits"""
def xor(a, b):
	res = bin(int(a, 2) ^ int(b, 2))[2:]
	while len(res) < len(a):
		res = '0' + res
	return res

"""left_rotation(bits, d)
   Realiza una rotación de un arreglo de bits hacia la izquierda.
   bits - Arreglo de bits
   d - Número de bits a rotar"""
def left_rotation(bits, d):
	aux, bits = bits[:d], bits[d:]
	return bits + aux

"""keys_generation(key)
   Genera las dos subllaves necesarias para el algoritmo de SDES.
   key - Llave de cifrado/descifrado(representada como bits)"""
def keys_generation(key):
	key = permutation(key, [2,4,1,6,3,9,0,8,7,5])
	l_key, r_key = key[:len(key)//2], key[len(key)//2:]
	l_key, r_key = left_rotation(l_key, 1), left_rotation(r_key, 1)
	key_1 = permutation(l_key + r_key, [5,2,6,3,7,4,9,8])
	l_key, r_key = left_rotation(l_key, 2), left_rotation(r_key, 2)
	key_2 = permutation(l_key + r_key, [5,2,6,3,7,4,9,8])
	return [key_1, key_2]

"""sdes(mode, text, keys)
   Realiza el cifrado y descifrado de Simplified DES.
   mode - Indica si se va a cifrar o descifrar, E (cifrar) y D (descifrar)
   text - Texto a cifrar/descifrar (representado como bits)
   keys - Subllaves para SDES"""
def sdes(mode, text, keys):
	text = permutation(text, [1,5,2,0,3,7,4,6])
	l_text, r_text = text[:len(text)//2], text[len(text)//2:]
	if mode == 'D':
		keys.reverse()
	for i in range(2):
		xor_key = xor(permutation(r_text, [3,0,1,2,1,2,3,0]), keys[i])
		sb = s_boxes(xor_key[:len(xor_key)//2], S0) + s_boxes(xor_key[len(xor_key)//2:], S1)
		l_text = xor(l_text, permutation(sb, [1,3,2,0]))
		if i == 0:
			l_text, r_text = r_text, l_text
	text = permutation(l_text + r_text, [3,0,2,4,6,1,7,5])
	return text

lines = list()
for line in fileinput.input():
	line = line.replace('\n', '')
	lines.append(line)
print(sdes(lines[0], lines[2], keys_generation(lines[1])))
