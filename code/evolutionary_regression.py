
import random
import math

class Line:

	def __init__(self, m: float, b: float, lb: int, ub: int) -> None:
		if m is None: m = random.uniform(lb, ub)
		if b is None: b = random.uniform(2*lb, 2*ub)
		self.m = m
		self.b = b
		self.lb = lb
		self.ub = ub
		self.error = math.inf


class Evol:

	def __init__(self, num_lines: int, num_populations: int, num_iter: int, data: str) -> None:
		self.num_lines = num_lines
		self.num_populations = num_populations
		self.num_iter = num_iter
		#self.population = [Line(None, None, -2, 2) for i in range(num_lines)]
		self.data = []
		with open(data) as file:
			for line in file.readlines():
				a, b = line.split()
				self.data += [(float(a), float(b))]

	def evaluate(self) -> None:
		for line in self.population:
			error = 0
			for (x, y) in self.data:
				y_estimate = line.m * x + line.b
				error += math.sqrt((y - y_estimate) ** 2)
			line.error = error

	def mutate(self, lines: list) -> None:
		for line in lines:
			mut_m = random.uniform(-0.2, 0.2)
			line.m += mut_m
			mut_b = random.uniform(-0.2, 0.2)
			line.b += mut_b

	def get_progeny(self, lines: list) -> list:
		# replicar as melhores linhas da população
		progeny = [Line(line.m, line.b, line.lb, line.ub) for line in lines]
		# recombinar linhas
		for i in range(0, len(progeny), 2):
			line1, line2 = progeny[i], progeny[i+1]
			# recombinação do valor de m
			m_mean = (line1.m + line2.m) / 2
			line1.m = line2.m = m_mean # ***
			# recombinação do valor de b
			b_mean = (line1.b + line2.b) / 2
			line1.b = line2.b = b_mean # ***
		# for loops para verificar se as linhas i e i+1 ficam diferentes após mutação (pointers ***)
		# for i, line in enumerate(progeny): print(f"before {i+1}: {line.m}")
		self.mutate(progeny)
		# for i, line in enumerate(progeny): print(f"after {i+1}: {line.m}")
		return progeny

	def new_population(self) -> None:
		best_lines = sorted(self.population, key = lambda x: x.error)[:self.num_lines//2]
		progeny = self.get_progeny(best_lines)
		self.population = best_lines + progeny

	def run_ea(self) -> list:
		best_error = math.inf
		best_pop = None
		for i in range(self.num_populations):
			# possibilidade de mudar os valores das lower (-2) e upper (2) bounds para retas com declive mais acentuado
			self.population = [Line(None, None, -2, 2) for i in range(self.num_lines)]
			for j in range(self.num_iter):
				self.evaluate()
				self.new_population()
			best_line = sorted(self.population, key = lambda x: x.error)[0]
			if best_line.error < best_error:
				best_error = best_line.error
				best_pop = self.population
		return best_pop

	def best_line(self) -> tuple:
		best_pop = self.run_ea()
		best_line = sorted(best_pop, key = lambda x: x.error)[0]
		return best_line.error, best_line.m, best_line.b


evol = Evol(num_lines=12, num_populations=10, num_iter=2000, data="regression_data2.txt")
#print(evol.data)
error, m, b = evol.best_line()
print(f"Error: {error:.2f}\nm: {m:.2f}\nb: {b:.2f}")

