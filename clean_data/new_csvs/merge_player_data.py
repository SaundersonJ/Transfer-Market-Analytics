import csv

# pass the transfermarkt file first

def merge_player_data(file1, file2, output_file,  *,
                      key1="Name",       # header in file1
                      key2="player_name" # header in file2
                      ):
    """
    Merge two CSVs on the player-name columns `key1` and `key2`
    and write the result to `output_file`.
    """

    def load(path, key):
        """Return {player_name: row_dict} for one CSV."""
        with open(path, newline='', encoding='utf-8-sig') as f:
            r = csv.DictReader(f, skipinitialspace=True)
            rows = {}
            for row in r:
                name = row[key].strip()
                row = {("name" if k == key else k): v for k, v in row.items()}
                rows[name] = row
        return rows

    data = load(file1, key1)             # start with file1’s rows
    for name, row in load(file2, key2).items():
        if name in data:
            # keep existing values unless the new one is non-blank
            for k, v in row.items():
                if v:                     # ignore empty strings
                    data[name][k] = v
        else:
            data[name] = row

    # Collect every column that ever appears, keep “name” first
    fieldnames = ['name'] + sorted({k for row in data.values() for k in row if k != 'name'})

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(data.values())

# Example call
merge_player_data(
    'transfermarkt_players_Bundesliga_22-23.csv',
    'understat_players_Bundesliga_2022-2023.csv',
    'merged_players.csv'
)
