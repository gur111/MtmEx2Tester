import random
import copy
import Olympics
import hw2comp
import os
import sys
import select


PLACES = [
    'Knowhere',
    'Israel_in_2050',
    '100_In_Infi',
    'Magnolia',
    'Camelot',
    'Nes_Tziona',
    'Narnia',
    'Wonderland',
    'Atlantis',
    'Georgies_Function_Whole',
    'Neverland',
    'Petah_Tikwa',
    'Krypton'
]

TYPES = ['untimed', 'timed', 'knockout']

ACTIVITIES = [
    'Pole_Sitting',
    'High_Swimming',
    'Not_Caring',
    'Rythmic_Running',
    'Chess',
    'Wall_Climbing',
    'Video_Gaming',
    'Bowling',
    'Bindge_Watching',
    'Breathe_Holding',
    'Delivery_Racing',
    'Human_Racing',
    'Technological_Racing',
    'Code_Writing',
    'The_Aryan_Racing',
    'Rat_Racing',
    'Mask_100M_Racing',
    'Phishing',
    'Manual_Array_Sorting',
    'Dancer_Circles_Counting',
    'Uniform_Converging',
    'Nuclear_Arm_Racing',
    'Space_Racing',
    'Long_Spitting',
    'Cup_Holding',
    'Manxplaining',
    'Bartending'
]


def get_competitor_string(competitor):
    competition_name = competitor['competition name']
    competition_type = competitor['competition type']
    competitor_id = competitor['competitor id']
    competitor_country = competitor['competitor country']
    result = competitor['result']

    return f'Competitor {competitor_id} from {competitor_country} participated in {competition_name} ({competition_type}) and scored {result}'


def get_competition_result(competition_name, winning_gold_country, winning_silver_country, winning_bronze_country):
    '''
    Given a competition name and its champs countries, the function prints the winning countries
        in that competition in a specific format.
    Arguments:
        competition_name: the competition name
        winning_gold_country, winning_silver_country, winning_bronze_country: the champs countries
    '''
    undef_country = 'undef_country'
    countries = [country for country in [winning_gold_country,
                                         winning_silver_country, winning_bronze_country] if country != undef_country]
    return f'The winning competitors in {competition_name} are from: {countries}'


def generate_test_file(test_file_path, out_file_path):
    places = random.sample(PLACES, k=random.randint(1, 12))
    activities = random.sample(ACTIVITIES, k=random.randint(0, 20))
    activities_types = [random.choice(TYPES) for _ in activities]

    competitors = []
    last_id = 0

    for _ in range(random.randint(1, 50)):
        last_id += random.randint(1, 100)
        competitors.append({'id': last_id,
                            'country': random.choice(places)})

    entries = []
    results = {}

    # for activity in activities:
    #     results[activity] = []
    results = {k: [] for k in activities}

    for i, activity in enumerate(activities):
        participated = set()
        last_measured = 0
        last_iter = random.randint(-1, len(competitors))

        for j in range(last_iter+1):
            competitor = random.choice(competitors)

            if activities_types[i] == 'knockout':
                measurement = j+1
            else:
                measurement = random.randint(last_measured+1, last_measured+10)

            if activities_types[i] in ['timed', 'knockout']:
                results[activity].append(competitor)
            elif activities_types[i] == 'untimed':
                results[activity].insert(0, competitor)

            if competitor['id'] in participated:
                try:
                    # If we have untimed we want to remove both the one just added and the first one
                    results[activity].remove(competitor)
                    results[activity].remove(competitor)
                except ValueError:
                    pass

            last_measured = measurement
            participated.add(competitor['id'])

            entries.append(
                f'competition {activity} {competitor["id"]} {activities_types[i]} {measurement}\n')

        if results[activity]:
            results[activity] += [{'country': 'undef_country'}]*2
            results[activity] = results[activity][0:3]
        else:
            del results[activity]

    # Create input file

    with open(test_file_path, 'w') as f:
        for competitor in competitors:
            f.write(f'competitor {competitor["id"]} {competitor["country"]}\n')

        for entry in entries:
            f.write(entry)

    # Create output file
    with open(out_file_path, 'w') as f:
        participants_int_competitions = hw2comp.readParseData(test_file_path)
        for competitor in sorted(participants_int_competitions, key=hw2comp.key_sort_competitor):
            string = get_competitor_string(competitor)
            f.write(string)
            f.write('\n')

        for competition_result_single in sorted([[x,
                                                  results[x][0]['country'],
                                                  results[x][1]['country'],
                                                  results[x][2]['country']] for x in results]):
            string = get_competition_result(*competition_result_single)
            f.write(string)
            f.write('\n')

        import Olympics
        olympics = Olympics.OlympicsCreate()
        pipe_out, stdout = redirect()

        for competition in results:
            Olympics.OlympicsUpdateCompetitionResults(
                olympics, str(results[competition][0]['country']),
                str(results[competition][1]['country']),
                str(results[competition][2]['country']))

        Olympics.OlympicsWinningCountry(olympics)
        Olympics.OlympicsDestroy(olympics)

        restore_stdout(stdout=stdout)
        # The output we got while redirecting
        f.write(read_pipe(pipe_out=pipe_out).decode())


def get_scrambled(file_name):
    import random
    with open(file_name, 'r') as source:
        data = [(random.random(), line) for line in source]
    data.sort()

    # split_file_name = os.path.splitext(file_name)
    scrambled_file_name = 'temp_scrambled.txt'
    with open(scrambled_file_name, 'w') as target:
        for _, line in data:
            target.write(line)

    return scrambled_file_name


def more_data(pipe_out):
    """ check if we have more to read from the pipe """
    r, _, _ = select.select([pipe_out], [], [], 0)
    return bool(r)

# read the whole pipe


def read_pipe(pipe_out):
    out = b''
    while more_data(pipe_out):
        out += os.read(pipe_out, 1024)

    return out


def redirect():
    sys.stdout.write(' \b')
    pipe_out, pipe_in = os.pipe()
    # save a copy of stdout
    stdout = os.dup(1)
    # replace stdout with our write pipe
    os.dup2(pipe_in, 1)

    return pipe_out, stdout


def restore_stdout(stdout):
    os.dup2(stdout, 1)


def get_scrambled(file_name, out_file='temp_scrambled.txt'):
    import random
    with open(file_name, 'r') as source:
        data = [(random.random(), line) for line in source]
    data.sort()

    # split_file_name = os.path.splitext(file_name)
    scrambled_file_name = out_file
    with open(scrambled_file_name, 'w') as target:
        for _, line in data:
            target.write(line)

    return scrambled_file_name



if __name__ == "__main__":
    generate_test_file('test1.txt', 'out1.txt')
    get_scrambled('test1.txt', 'test1.txt')

