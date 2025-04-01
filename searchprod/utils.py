from fuzzywuzzy import process

def search_with_fuzzy(user_input, reference_list, score_threshold=75):
    closest_matches = process.extract(user_input, reference_list)
    # Filter out matches with scores below the threshold
    filtered_matches = [match for match in closest_matches if match[1] >= score_threshold]
    return filtered_matches
