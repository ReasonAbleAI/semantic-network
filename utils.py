from flask import jsonify

def build_search_where_clause(args):
    input_query = args.get('query')
    keywords = args.get('keywords')
    min_credibility = args.get('min_credibility')
    min_accuracy = args.get('min_accuracy')
    min_authenticity = args.get('min_authenticity')
    min_confidence = args.get('min_confidence')
    min_relevance = args.get('min_relevance')
    type = args.get('type')
    regex = args.get('regex')

    where_caluses = []
    params = {}
    if input_query:
        where_caluses.append("(n.document CONTAINS $query)")
        params["query"] = input_query
    if keywords:
        where_caluses.append(f"any(keyword IN n.keywords WHERE keyword IN $keywords)")
        params["keywords"] = keywords.split(",")
    if min_credibility is not None:
        where_caluses.append(f"n.credibility >= $min_credibility")
        params["min_credibility"] = min_credibility
    if min_accuracy is not None:
        where_caluses.append(f"n.accuracy >= $min_accuracy")
        params["min_accuracy"] = min_accuracy
    if min_authenticity is not None:
        where_caluses.append(f"n.authenticity >= $min_authenticity")
        params["min_authenticity"] = min_authenticity
    if min_confidence is not None:
        where_caluses.append(f"n.confidence >= $min_confidence")
        params["min_confidence"] = min_confidence
    if min_relevance is not None:
        where_caluses.append(f"n.relevance >= $min_relevance")
        params["min_relevance"] = min_relevance
    if type:
        where_caluses.append(f"n.type = $type")
        params["type"] = type
    if regex:
        where_caluses.append(f"(n.document =~ $regex)")
        params["regex"] = regex

    if not where_caluses:
        return jsonify({"error": "At least one of the following arguments must be provided 'query', 'keywords', 'regex', or 'min_credibility'"}), 400

    return where_caluses, params
