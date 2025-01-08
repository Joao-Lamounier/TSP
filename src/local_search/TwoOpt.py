from .LocalSearch import LocalSearch


class TwoOpt(LocalSearch):

    def __init__(self, distance_matrix, run_time, path, objective_function):
        self.distance_matrix = distance_matrix
        self.run_time = run_time
        self.objective_function = objective_function
        self.path = path
        self.n = len(path)

    def solve_two_opt(self):

        route = self.path[:]
        best_distance = self.objective_function

        improved = True
        while improved:
            improved = False

            for i in range(0, self.n - 1):
                for j in range(i + 1, self.n):

                    new_route = route[:i] + list(reversed(route[i:j])) + route[j:]
                    new_distance = self.calculate_distance(new_route, self.distance_matrix)

                    if new_distance < best_distance:
                        route = new_route
                        best_distance = new_distance
                        improved = True
                        break

                if improved:
                    break

        self.path, self.objective_function = route, best_distance
