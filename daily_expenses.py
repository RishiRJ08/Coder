import math
from datetime import date

def get_cost(prompt):
	while True:
		try:
			val = input(prompt).strip()
			if val == "":
				return 0.0
			cost = float(val)
			if cost < 0:
				print("Please enter a non-negative value.")
				continue
			return cost
		except ValueError:
			print("Invalid number. Try again.")

def main():
	today = date.today().isoformat()
	print(f"Daily expenses for {today}")
	cab = get_cost("Enter cab cost: ")
	shopping = get_cost("Enter shopping cost: ")
	meal = get_cost("Enter meal cost: ")
	total = math.fsum([cab, shopping, meal])

	print("\nBreakdown:")
	print(f" - Cab:      ${cab:.2f}")
	print(f" - Shopping: ${shopping:.2f}")
	print(f" - Meal:     ${meal:.2f}")
	print(f"Total for today: ${total:.2f}")

if __name__ == "__main__":
	main()
