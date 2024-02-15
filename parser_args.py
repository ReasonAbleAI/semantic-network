from webargs import fields, validate
from datetime import datetime

node_args = {
    "document": fields.Str(required=True),
    "keywords": fields.List(fields.Str(), load_default=[]),
    "source": fields.Str(allow_none=True),
    "credibility": fields.Float(validate=validate.Range(min=0, max=1), allow_none=True),
    "accuracy": fields.Float(validate=validate.Range(min=0, max=1), allow_none=True),
    "authenticity": fields.Float(validate=validate.Range(min=0, max=1), allow_none=True),
    "confidence": fields.Float(validate=validate.Range(min=0, max=1), allow_none=True),
    "relevance": fields.Float(validate=validate.Range(min=0, max=1), allow_none=True),
    "type": fields.Str(allow_none=True),
    "created_at": fields.DateTime(load_default=datetime.utcnow),
}

relationship_args = {
    "target_id": fields.Int(required=True),
    "weight": fields.Float(validate=validate.Range(min=0, max=1), load_default=None),
    "accuracy": fields.Float(validate=validate.Range(min=0, max=1), load_default=None),
    "authenticity": fields.Float(validate=validate.Range(min=0, max=1), load_default=None),
    "confidence": fields.Float(validate=validate.Range(min=0, max=1), load_default=None),
    "relevance": fields.Float(validate=validate.Range(min=0, max=1), load_default=None),
    "credibility": fields.Float(validate=validate.Range(min=0, max=1), load_default=None),
    "reasoning": fields.Str(load_default=None),
    "created_at": fields.DateTime(load_default=datetime.utcnow),
}

search_args = {
    "query": fields.Str(load_default=None),
    "keywords": fields.Str(load_default=None),
    "min_credibility": fields.Float(validate=validate.Range(min=0, max=1), load_default=None),
    "min_accuracy": fields.Float(validate=validate.Range(min=0, max=1), load_default=None),
    "min_authenticity": fields.Float(validate=validate.Range(min=0, max=1), load_default=None),
    "min_confidence": fields.Float(validate=validate.Range(min=0, max=1), load_default=None),
    "min_relevance": fields.Float(validate=validate.Range(min=0, max=1), load_default=None),
    "type": fields.Str(load_default=None),
    "regex": fields.Str(load_default=None),
}