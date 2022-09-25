# -*- coding: utf-8 -*-

import math
import random


class Point:

	"""
	Define um ponto em R(2) - point=(x,y) - e indica a que cluster de pontos pertence.
	"""

	def __init__(self, x: float, y: float, cluster: int = 0) -> None:
		self.x = x
		self.y = y
		self.cluster = cluster


class KMeans:

	"""
	Implementa o algoritmo K-Means Clustering. Apenas incluí um método público (generate_code()), que gera código Python que
	permite a criação de um plot contendo os pontos introduzidos pelo utilizador e indicação dos clusters ao quais os mesmos
	pertencem (através da representação de círculos no plot).
	"""

	def __init__(self, data: str, num_clusters: int) -> None:
		self.data = []
		points = open(data).readlines()
		for point in points:
			if point.split():
				x, y = point.split()
				msg = f"ERRO: As coordenadas ('{x}', '{y}') são inválidas."
				assert x.isdigit() and y.isdigit(), msg
				self.data += [Point(float(x), float(y))]
		assert type(num_clusters) is int, "ERRO: O parâmetro 'num_clusters' deve ser do tipo 'int'."
		self.num_clusters = num_clusters

	def __get_centroids(self) -> None:
		x_coords = random.sample(range(12), self.num_clusters)
		y_coords = random.sample(range(12), self.num_clusters)
		self.centroids = {i+1: (x_coords[i], y_coords[i]) for i in range(self.num_clusters)}

	def __evaluate_points(self) -> int:
		diff = 0 # ***
		for point in self.data:
			min_dist = math.inf
			cluster = None
			for cent in self.centroids:
				# Manhattan distances (|x(point)-x(centroid)| + |y(point)-y(centroid)|)
				dist = abs(point.x - self.centroids[cent][0]) + abs(point.y - self.centroids[cent][1])
				if dist < min_dist:
					min_dist = dist
					cluster = cent
			# de modo a verificar se se alterou o cluster a que algum ponto pertence ***
			if point.cluster != cluster: diff += 1
			point.cluster = cluster
		return diff # ***

	def __update_centroids(self) -> None:
		# self.clusters tem de ser redefinido sempre que se atualizam os centróides (para que as listas alberguem novos pontos)
		# dicionário em que as keys são os identificadores dos centróides e os values são listas de pontos
		self.clusters = {i+1: [] for i in range(self.num_clusters)}
		for point in self.data:
			self.clusters[point.cluster] += [point]
		# atualizar as coordenadas dos centróides fazendo as médias de x e y para cada um dos clusters de pontos
		for cluster in self.clusters:
			x = y = 0
			size = len(self.clusters[cluster])
			for point in self.clusters[cluster]:
				x += point.x
				y += point.y
			if size: self.centroids[cluster] = (x/size, y/size)

	def __run_k_means(self) -> None:
		# definição de um novo atributo self.centroids (caso algum dos clusters - cuja key é o identificador de um centróide - não 
		# contenha qualquer ponto, redefine-se self.centroids +++) cujas coordenadas iniciais são escolhidas de forma aleatória
		self.__get_centroids()
		while True:
			diff = self.__evaluate_points()
			if not diff: break
			self.__update_centroids()
			if any(not self.clusters[cluster] for cluster in self.clusters): # +++
				self.__get_centroids()

	def __get_circles(self) -> dict:
		self.__run_k_means()
		distances = {k: [v] for k, v in self.centroids.items()}
		for cluster in self.clusters:
			max_dist = 0
			for point in self.clusters[cluster]:
				# Manhattan distances (|x(point)-x(centroid)| + |y(point)-y(centroid)|)
				dist = abs(point.x - self.centroids[cluster][0]) + abs(point.y - self.centroids[cluster][1])
				if dist > max_dist:
					max_dist = dist
			distances[cluster] += [max_dist]
		return distances

	def __get_points(self) -> tuple:
		x, y = [], []
		for point in self.data:
			x += [point.x]
			y += [point.y]
		return x, y

	def generate_code(self) -> None:
		print("from matplotlib import pyplot as plt\nfrom IPython.display import clear_output")
		print("ax = plt.gca()")
		x, y = self.__get_points()
		print(f"x_coords = {x}\ny_coords = {y}")
		print("ax.scatter(x_coords, y_coords)")
		circles = self.__get_circles()
		add_patches = []
		for circle in circles:
			if not circles[circle][1]: circles[circle][1] = 0.4
			print(f"circle{circle} = plt.Circle({circles[circle][0]}, {circles[circle][1]}, fill=False)")
			add_patches += [f"ax.add_patch(circle{circle})"]
		print("\n".join(add_patches))
		print("clear_output()")


if __name__ == "__main__":
	km = KMeans(data="k_means_data1.txt", num_clusters=4)
	km.generate_code()
	#print(km.clusters)
