"""Review class"""


class Review(object):
    """Represents a review in the repository"""

    def __init__(self):
        self._submission = ''
        self._review_request1 = ''
        self._review_request2 = ''
        self._review_response1 = ''
        self._review_response2 = ''
        self._evaluation_result = ''

    @property
    def submission(self):
        """Submission message"""
        return self._submission

    @property
    def review_request1(self):
        """Message for review request 1"""
        return self._review_request1

    @property
    def review_request2(self):
        """Message for review request 2"""
        return self._review_request2

    @property
    def review_response1(self):
        """Message for review response 1"""
        return self._review_response1

    @property
    def review_response2(self):
        """Message for review response 2"""
        return self._review_response2

    @property
    def evaluation_result(self):
        """Message for evaluation results"""
        return self._evaluation_result

    def set_submission(self, message):
        """Set submission message"""
        if not self._submission and message:
            self._submission = message
        else:
            raise ValueError('Invalid request')

    def set_review_request_1(self, message):
        """Set message for review request 1"""
        if not self._review_request1 and self._submission and message:
            self._review_request1 = message
        else:
            raise ValueError('Invalid request')

    def set_review_request_2(self, message):
        """Set message for review request 2"""
        if not self._review_request2 and self._review_request1 and message:
            self._review_request2 = message
        else:
            raise ValueError('Invalid request')

    def set_review_response_1(self, message):
        """Set message for review response 1"""
        if not self._review_response1 and self._review_request1 and message:
            self._review_response1 = message
        else:
            raise ValueError('Invalid request')

    def set_review_response_2(self, message):
        """Set message for review response 2"""
        if not self._review_response2 and self._review_request2 and message:
            self._review_response2 = message
        else:
            raise ValueError('Invalid request')

    def set_evaluation_result(self, message):
        """Set message for evaluation results"""
        if not self._evaluation_result and self._review_response1 \
                and self._review_response2 and message:
            self._evaluation_result = message
        else:
            raise ValueError('Invalid request')
