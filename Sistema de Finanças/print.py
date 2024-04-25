print(f"{'Descrição':^^20} | {'Valor':^6} | {'Data':12}")
print(f"{'-'*20} | {'-'*6} | {'-'*12}")

for row in ganho:
    print(f"({row[0]:<20} | {row[1]:^6} | {row[2]:>12})")