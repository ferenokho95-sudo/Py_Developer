import re

def nums(version):
    if not version:
        version = ""
    parts = re.findall(r"\d+", version)
    return tuple(map(int, parts))


def vkey(version):
    numbers = list(nums(version))
    while numbers and numbers[-1] == 0:
        numbers.pop()
    return tuple(numbers)


def branch_depth(fixes):
    seen = set()
    for fixed in fixes:
        seen.add(nums(fixed))
    if len(seen) < 2:
        return 1

    depth = 1
    while True:
        branches = set()
        for version in seen:
            branches.add(version[:depth])
        if len(branches) == len(seen):
            return depth
        depth += 1


def range_hit(version, start, fixed):
    version_key = vkey(version)
    if version_key < vkey(start):
        return False
    if fixed is None:
        return True
    return version_key < vkey(fixed)


def advisory_hit(version, ranges):
    fixes = []
    for start, fixed in ranges:
        if fixed:
            fixes.append(fixed)

    depth = branch_depth(fixes)
    branch = nums(version)[:depth]
    for start, fixed in ranges:
        if fixed and nums(fixed)[:depth] == branch:
            if range_hit(version, start, fixed):
                return fixed
            return None

    hit = False
    fix = ""
    for start, fixed in ranges:
        if not range_hit(version, start, fixed):
            continue
        hit = True
        if fixed:
            if not fix or vkey(fixed) < vkey(fix):
                fix = fixed
    if not hit:
        return None
    return fix
