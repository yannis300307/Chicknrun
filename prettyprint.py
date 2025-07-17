
def error(*args):
	print(f"\x1B[31;1m{''.join([str(arg) for arg in args])}\x1B[0m")

def warn(*args):
	print(f"\x1B[93;1m{''.join([str(arg) for arg in args])}\x1B[0m")

def info(*args):
	print(f"\x1B[94m{''.join([str(arg) for arg in args])}\x1B[0m")

def success(*args):
	print(f"\x1B[92;1m{''.join([str(arg) for arg in args])}\x1B[0m")

def ask(*args):
	return input(f"\x1B[35;1m{''.join([str(arg) for arg in args])}\x1B[0m").strip().lower()
