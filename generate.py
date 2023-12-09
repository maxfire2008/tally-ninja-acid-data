from faker import Faker
import yaml
import random
import os
import pathlib
import PIL.Image
import PIL.ImageDraw


def generate_athletes():
    # Generate 5000 fake people with a name, dob, gender, team (red, blue, green, yellow) each
    fake = Faker()
    teams = ["red", "blue", "green", "yellow"]
    for _ in range(10000):
        # Generate fake gender
        gender = random.choice(["male", "female"]) if random.random() > 0.1 else "other"

        surname = fake.last_name()

        if gender == "male":
            # Generate fake name
            name = fake.first_name_male() + (
                " " + surname if random.random() > 0.1 else ""
            )
        elif gender == "female":
            name = fake.first_name_female() + (
                " " + surname if random.random() > 0.1 else ""
            )
        else:
            name = fake.name_nonbinary() + (
                " " + surname if random.random() > 0.1 else ""
            )

        # Generate fake date of birth
        dob = fake.date_of_birth(minimum_age=8, maximum_age=80)

        # Choose a random team color
        team = random.choice(teams)

        filename = "".join((x if x.isalnum() else "_") for x in name).lower() + ".yaml"
        # export data to yaml file
        with open("output/athletes/" + filename, "w") as f:
            yaml.dump(
                {
                    "name": name,
                    "dob": dob,
                    "gender": gender,
                    "team": team,
                },
                f,
                default_flow_style=False,
                sort_keys=False,
            )


def generate_athlete_photos():
    athletes = os.listdir("output/athletes")

    for athlete in athletes:
        athlete = athlete.split(".")[0]

        # generate between 3 and 20 circles of random size and colour scattered across the image
        # save as <athlete>.jpeg

        photo = PIL.Image.new("RGB", (128, 128), color="white")
        draw = PIL.ImageDraw.Draw(photo)

        for _ in range(random.randint(3, 20)):
            x = random.randint(0, 128)
            y = random.randint(0, 128)
            radius = random.randint(5, 20)
            colour = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=colour)

        photo.save("output/athlete_photos/" + athlete + ".jpeg")


def generate_races():
    fake = Faker()
    # get a list of all the athletes
    athletes = os.listdir("output/athletes")

    for i in range(100):
        data = {
            "type": "race",
            "name": "Race " + str(i),
            "distance": "100m",
            "date": fake.date_between(start_date="-1y", end_date="today"),
            "results": {},
        }

        for j in range(100):
            athlete = random.choice(athletes)
            athlete = athlete.split(".")[0]
            data["results"][athlete] = {
                "finish_time": random.randint(10000, 60000),
            }

            if random.random() > 0.05:
                data["results"][athlete][random.choice(["DNF", "DNS", "DQ"])] = True

        with open("output/results/race_" + str(i) + ".yaml", "w") as f:
            yaml.dump(
                data,
                f,
                default_flow_style=False,
                sort_keys=False,
            )


if __name__ == "__main__":
    pathlib.Path("output/athletes").mkdir(parents=True, exist_ok=True)
    pathlib.Path("output/athlete_photos").mkdir(parents=True, exist_ok=True)
    pathlib.Path("output/results").mkdir(parents=True, exist_ok=True)

    generate_athletes()
    generate_athlete_photos()
    generate_races()
