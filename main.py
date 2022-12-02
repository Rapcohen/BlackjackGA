import time

from ga import evolution_algo

if __name__ == "__main__":
    start_time = time.time()
    evolution_algo().evolve()
    print("--- execution time: %.2f seconds ---" % (time.time() - start_time))
