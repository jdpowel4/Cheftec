def score_matches(ingredients):
    scores = {}

    for ingredient in ingredients:
        scores.setdefault(ingredient.id, {
            "ingredient": ingredient,
            "score": 0
        })
        scores[ingredient.id]["score"] += 1

    return sorted(
        scores.values(),
        key=lambda x: x["score"],
        reverse=True
    )