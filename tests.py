import unittest
import os
import finbox_bankconnect as bc
from finbox_bankconnect.custom_exceptions import EntityNotFoundError
from finbox_bankconnect.utils import is_valid_uuid4

class TestUtilFunctions(unittest.TestCase):
    """
    Test cases for utility functions
    """

    def is_valid_uuid4(self):
        self.assertEqual(is_valid_uuid4("c036e96d-ccae-443c-8f64-b98ceeaa1578"), True, "valid uuid4 detected as invalid")

    def test_uuid4_without_hyphen(self):
        self.assertEqual(is_valid_uuid4("c036e96dccae443c8f64b98ceeaa1578"), False, "valid uuid4 without hyphen must be invalid")

    def test_string_not_uuid4(self):
        self.assertEqual(is_valid_uuid4("abc"), False, "invalid uuid4 string detected as valid")

    def test_integer(self):
        self.assertEqual(is_valid_uuid4(123), False, "integer detected as valid uui4")

    def test_list(self):
        self.assertEqual(is_valid_uuid4(["sadasd", "asdasd"]), False, "list detected as valid uui4")

    def test_none(self):
        self.assertEqual(is_valid_uuid4(None), False, "list detected as valid uui4")

class TestGetEntityEdgeCases(unittest.TestCase):
    """
    Test edge cases for Entity.get function
    """

    def setUp(self):
        bc.api_key = os.environ['TEST_API_KEY']

    def test_empty_entity_id(self):
        exception_handled = False
        try:
            bc.Entity.get(entity_id = '')
        except ValueError:
            exception_handled = True
        self.assertEqual(exception_handled, True, "entity_id blank string case - not handled")

    def test_none_entity_id(self):
        exception_handled = False
        try:
            bc.Entity.get(entity_id = None)
        except ValueError:
            exception_handled = True
        self.assertEqual(exception_handled, True, "entity_id none case - not handled")

    def test_invalid_entity_id(self):
        exception_handled = False
        try:
            bc.Entity.get(entity_id = 'c036e96dccae443c8f64b98ceeaa1578')
        except ValueError:
            exception_handled = True
        self.assertEqual(exception_handled, True, "entity_id not a valid uuid4 (with hyphen) case - not handled")

    def test_non_string_entity_id(self):
        list_handled = False
        int_handled = False
        try:
            bc.Entity.get(entity_id = ["hello"])
        except ValueError:
            list_handled = True
        try:
            bc.Entity.get(entity_id = 123)
        except ValueError:
            int_handled = True
        self.assertEqual(list_handled and int_handled, True, "entity_id non string case - not handled")

    def test_detail_not_found(self):
        exception_handled = False
        try:
            entity = bc.Entity.get(entity_id = 'c036e96d-ccae-443c-8f64-b98ceeaa1578')
            entity.get_transactions()
            # assuming this uuid id doesn't exists in DB :P
        except EntityNotFoundError:
            exception_handled = True
        self.assertEqual(exception_handled, True, "entity_id valid but not in DB case - not handled")

class TestLinkIdFlow(unittest.TestCase):
    """
    Test the flow by using the link_id
    """

    def setUp(self):
        bc.api_key = os.environ['TEST_API_KEY']

    def test_non_string_link_id(self):
        list_handled = False
        int_handled = False
        try:
            bc.Entity.create(link_id = ["hello"])
        except ValueError:
            list_handled = True
        try:
            bc.Entity.create(link_id = 123)
        except ValueError:
            int_handled = True
        self.assertEqual(list_handled and int_handled, True, "link_id non string case - not handled")

    def test_entity_creation(self):
        entity = bc.Entity.create(link_id = "python_link_id_test")
        entity_id = entity.entity_id
        self.assertEqual(is_valid_uuid4(entity_id), True, "entity_id couldn't be created against the link_id")

    def test_link_id_fetch(self):
        entity = bc.Entity.get(entity_id=os.environ['TEST_ENTITY_ID'])
        self.assertEqual(entity.link_id, None, "link_id was incorrectly fetched")

class TestIdentity(unittest.TestCase):
    """
    Test identity when using get_accounts function
    """
    def setUp(self):
        bc.api_key = os.environ['TEST_API_KEY']
        entity = bc.Entity.get(entity_id=os.environ['TEST_ENTITY_ID'])
        self.identity = entity.get_identity()

    def check_name(self):
        self.assertIn("name", self.identity, "name not present in identity")

    def check_account_id(self):
        self.assertIn("account_id", self.identity, "account_id not present in identity")

    def check_account_number(self):
        self.assertIn("account_number", self.identity, "account_number not present in identity")

    def check_address(self):
        self.assertIn("address", self.identity, "address not present in identity")

class TestAccounts(unittest.TestCase):
    """
    Test accounts when using get_accounts function
    """
    def setUp(self):
        bc.api_key = os.environ['TEST_API_KEY']
        entity = bc.Entity.get(entity_id=os.environ['TEST_ENTITY_ID'])
        self.first_account = next(entity.get_accounts())

    def check_months(self):
        self.assertIn("months", self.first_account, "months not present in account")

    def check_account_id(self):
        self.assertIn("account_id", self.first_account, "account_id not present in account")

    def check_account_number(self):
        self.assertIn("account_number", self.first_account, "account_number not present in account")

class TestFraudInfo(unittest.TestCase):
    """
    Test fraud info when using get_accounts function
    """
    def setUp(self):
        bc.api_key = os.environ['TEST_API_KEY']
        entity = bc.Entity.get(entity_id=os.environ['TEST_ENTITY_ID'])
        self.first_fraud = next(entity.get_fraud_info())

    def check_fraud_type(self):
        self.assertIn("fraud_type", self.first_fraud, "months not present in fraud")

    def check_statement_id(self):
        self.assertIn("statement_id", self.first_fraud, "statement_id not present in fraud")

class TestFetchTransactions(unittest.TestCase):
    """
    Test transaction response when using get_transactions function
    """

    def setUp(self):
        bc.api_key = os.environ['TEST_API_KEY']
        entity = bc.Entity.get(entity_id=os.environ['TEST_ENTITY_ID'])
        self.first_transaction = next(entity.get_transactions())

    def test_balance_exists(self):
        self.assertIn("balance", self.first_transaction, "balance not present in transaction")

    def test_transaction_type_exists(self):
        self.assertIn("transaction_type", self.first_transaction, "balance not present in transaction")

    def test_date_exists(self):
        self.assertIn("date", self.first_transaction, "balance not present in transaction")

if __name__ == '__main__':
    unittest.main()
