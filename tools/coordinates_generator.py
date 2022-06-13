import psycopg2
import random
from uuid import uuid4

INT_MIN = -2147483648
INT_MAX = 2147483647


def get_random_int() -> int:
    return random.randint(INT_MIN, INT_MAX)


def get_random_name() -> str:
    return f"random-point-{str(uuid4())}"


def generate_coordinates(limit: int) -> None:
    conn = psycopg2.connect(database="pathfinder_db", user="postgres", password="secret", host="127.0.0.1", port="5432")

    for coord_index in range(limit):
        name = get_random_name()

        while True:
            x_coord = get_random_int()
            y_coord = get_random_int()

            cur = conn.cursor()

            cur.execute(f"""
                SELECT COUNT(1) FROM coordinates WHERE x_coord = {x_coord} AND y_coord = {y_coord} LIMIT 1
            """)

            (result, ) = cur.fetchone()

            if not result:
                break
        
        cur.execute(f"""
            INSERT INTO coordinates (id, name, x_coord, y_coord)
            VALUES ('{str(uuid4())}', '{name}', {x_coord}, {y_coord});
        """)

        conn.commit()




def main() -> None:
    generate_coordinates(500)


if __name__ == "__main__":
    main()
