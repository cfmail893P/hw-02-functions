import subprocess
import sys
import json
import pathlib
from os import environ
import difflib
import os


def update_score(db_path, student, problem_id, score):
    import sqlite3

    conn = sqlite3.connect(db_path)
    try:


        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS results (
                student    TEXT    NOT NULL,
                problem_id INTEGER NOT NULL,
                status     BOOLEAN DEFAULT NULL,
                PRIMARY KEY (problem_id, student)
            )
            """
        )

        conn.execute(
            """
            INSERT INTO results (student, problem_id, status)
            VALUES (?, ?, ?)
            ON CONFLICT(student, problem_id)
            DO UPDATE SET status = excluded.status
            """,
            (student, problem_id, score),
        )


        conn.commit()
    finally:
        conn.close()


def print_diff(expected, actual):
    print(f"--- Test FAILED ---")
    diff = difflib.unified_diff(
        expected.splitlines(keepends=True),
        actual.splitlines(keepends=True),
        fromfile="expected",
        tofile="actual",
    )
    sys.stdout.writelines(diff)
    print()

def run_case(binary, timeout=5):
    try:
        result = subprocess.run(
            [binary], capture_output=True,
            text=True, timeout=timeout
        )
    except subprocess.TimeoutExpired:
        return False, "timeout"
    ok = result.returncode == 0
    return ok, result.stdout


def main():
    if len(sys.argv) < 2:
        print("Usage: run_tests.py <binary>")
        sys.exit(2)

    binary = sys.argv[1]

    ok, test_output = run_case(binary)

    print(test_output)


    if "SAVE_SCORE_DB" in environ:
        if len(sys.argv) < 4:
            print("Usage: run_tests.py <binary> <student> <problem_id>")
            sys.exit(2)

        student = sys.argv[2]
        problem_id = sys.argv[3]
        db_path = environ["SAVE_SCORE_DB"]
        db_path_resolved = os.path.abspath(os.path.expanduser(db_path))

        print(f'Student: {student}')
        print(f'Problem id: {problem_id}')
        print(f'DB file {db_path}')
        print("DB path resolved to:", db_path_resolved)

        update_score(db_path_resolved, student, problem_id, ok)


    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
