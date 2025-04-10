import difflib

def closest_match(input_city: str,
                        city_list: list, 
                        cutoff: float = 0.7):
    matches = difflib.get_close_matches(input_city, city_list, n=1, cutoff=cutoff)
    
    if matches:
        return matches
    else:
        return None