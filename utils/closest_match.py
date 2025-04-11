from difflib import get_close_matches

def closest_match(input_city: str, city_list: list):
    matches = get_close_matches(input_city, city_list, n=1, cutoff=0.7)
    
    if matches:
        return matches[0]
    else:
        return None