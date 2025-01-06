from typing import Dict, Tuple, List
from datetime import datetime
import calendar
from src.utils import group_solutions, list_range


class Scheduler:
    def __init__(
        self,
        solution: Dict[str, int] | None,
        month: int | None = 4,
        year: int | None = 2019,
        num_personnel: int = 80,
        num_sections: int = 7,
        num_shifts: int = 2,
    ):
        self.solution = solution
        self.X, self.h, self.d = group_solutions(solution)
        self.year: int = year
        self.month: int = month  # April 2019 consists of 30 days and start at monday
        self.first_day = datetime(self.year, self.month, 1)
        self.first_weekday = self.first_day.weekday()
        self.num_days = calendar.monthrange(year, month)[1]
        self.num_personnel = num_personnel
        self.num_sections = num_sections
        self.num_shifts = num_shifts
        self.weekdays = list(calendar.day_name)
        self.schedule = self.empty_schedule
        self.file_name: str = f"shift_schedule_{self.month}_{self.year}.xlsx"
        self.night_shifts = {}
        self.day_shifts = {}

    @property
    def rows_per_person(self) -> int:
        return (self.num_days + self.first_weekday + 6) // 7

    @property
    def empty_schedule(self):
        schedule = {day: [] for day in self.weekdays}
        for _ in range(self.num_personnel):
            for day in self.weekdays:
                schedule[day].extend([""] * self.rows_per_person)
        return schedule

    def cell_value(self, i: int, j: int) -> str:
        cell_val = []
        for k in list_range(self.num_sections):
            for l in list_range(self.num_shifts):
                shift_val = round(self.X[f"X_{i}_{j}_{k}_{l}"])
                leave_val = round(self.h[f"h_{i}_{j}"])
                if leave_val > 0 and len(cell_val) == 0:
                    cell_val.append("X")
                elif shift_val and shift_val > 0:
                    if l == 1:
                        day_shift = self.day_shifts.get(i, 0)
                        self.day_shifts[i] = day_shift + 1
                    if l == 2:
                        night_shift = self.night_shifts.get(i, 0)
                        self.night_shifts[i] = night_shift + 1
                    cell_val.append(f"{k}({l})")
        return "".join(cell_val)

    def update_schedule(self, p: int, day: int, row: int, col: int):
        current_row = (p * self.rows_per_person) + row
        self.schedule[self.weekdays[col]][current_row] = self.cell_value(p + 1, day)

    def get_schedule(self) -> Tuple[Dict[str, list], List[List[int]]]:
        for p in range(self.num_personnel):
            day = 1
            for row in range(self.rows_per_person):
                for col in range(7):
                    if row == 0 and col < self.first_weekday:
                        continue
                    if day > self.num_days:
                        break
                    self.update_schedule(p, day, row, col)
                    day += 1
                if day > self.num_days:
                    break

        return self.schedule
