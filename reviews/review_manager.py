"""Module for managing reviews in the repository"""

import os
from iniformat.writer import write_ini_file
from iniformat.reader import read_ini_file
from reviews.review import Review


class ReviewManager(object):
    """Manage reviews"""

    def __init__(self, path, user_manager, document_manager):
        self._storage_location = path
        self._user_manager = user_manager
        self._document_manager = document_manager
        self._review = Review()
        self._document_id = None

    def select_document(self, document_id):
        """Chose which document to work on"""
        review_path = os.path.join(self._storage_location, "{}.rev".format(document_id))
        self._document_id = document_id
        if os.path.exists(review_path):
            self.load_review(review_path)

    def submit_document(self, author_id, manager_id, document_id):
        """Submit document for review"""
        if self._user_manager.has_role(author_id, 'author') and \
                self._user_manager.has_role(manager_id, 'manager'):
            message = "submission: {} from {} to {}".format(document_id, author_id, manager_id)
            self._review.set_submission(message)
        else:
            raise ValueError("Invalid operation")

    def send_reviewing_request_1(self, manager_id, reviewer_id, request_id):
        """Request review 1"""
        if self._user_manager.has_role(manager_id, 'manager') and \
                self._user_manager.has_role(reviewer_id, 'reviewer'):
            message = "request1: {} from {} to {}".format(request_id, manager_id, reviewer_id)
            self._review.set_review_request_1(message)
        else:
            raise ValueError("Invalid operation")

    def send_reviewing_request_2(self, manager_id, reviewer_id, request_id):
        """Request review2"""
        if self._user_manager.has_role(manager_id, 'manager') and \
                self._user_manager.has_role(reviewer_id, 'reviewer'):
            message = "request2: {} from {} to {}".format(request_id, manager_id, reviewer_id)
            self._review.set_review_request_2(message)
        else:
            raise ValueError("Invalid operation")

    def send_review_1(self, reviewer_id, manager_id, review_id):
        """"Response to request 1"""
        if self._user_manager.has_role(reviewer_id, 'reviewer') and \
                self._user_manager.has_role(manager_id, 'manager'):
            message = "review1: {} from {} to {}".format(review_id, reviewer_id, manager_id)
            self._review.set_review_response_1(message)
        else:
            raise ValueError("Invalid operation")

    def send_review_2(self, reviewer_id, manager_id, review_id):
        """Response to request 2"""
        if self._user_manager.has_role(reviewer_id, 'reviewer') and \
                self._user_manager.has_role(manager_id, 'manager'):
            message = "review2: {} from {} to {}".format(review_id, reviewer_id, manager_id)
            self._review.set_review_response_2(message)
        else:
            raise ValueError("Invalid operation")

    def send_evaluation(self, manager_id, author_id, evaluation_id):
        """Response to submission"""
        if self._user_manager.has_role(manager_id, 'manager') and \
                self._user_manager.has_role(author_id, 'author'):
            message = "evaluation: {} from {} to {}".format(evaluation_id, manager_id, author_id)
            self._review.set_evaluation_result(message)
        else:
            raise ValueError("Invalid operation")

    def load_review(self, review_path):
        """Load review status from file"""
        review_data = read_ini_file(review_path)
        self._review.submission = review_data['review']['submission']
        self._review.review_request1 = review_data['review']['request1']
        self._review.review_request2 = review_data['review']['request2']
        self._review.review_response1 = review_data['review']['response1']
        self._review.review_response2 = review_data['review']['response2']
        self._review.evaluation_result = review_data['review']['result']

    def save_review(self):
        """Save review status to disk"""
        review_info = {'review':{}}
        review_info['review']['submission'] = self._review.submission
        review_info['review']['request1'] = self._review.review_request1
        review_info['review']['request2'] = self._review.review_request2
        review_info['review']['response1'] = self._review.review_response1
        review_info['review']['response2'] = self._review.review_response2
        review_info['review']['result'] = self._review.evaluation_result
        review_path = os.path.join(self._storage_location, "{}.rev".format(self._document_id))
        write_ini_file(review_path, review_info)
