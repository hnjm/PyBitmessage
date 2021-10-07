from .telenium_process import TeleniumTestProcess
from .common import skip_screen_checks
from .common import ordered

test_address = {
    'invalid_address': 'BM-2cWmjntZ47WKEUtocrdvs19y5CivpKoi1',
    'autoresponder_address': 'BM-2cVWtdUzPwF7UNGDrZftWuHWiJ6xxBpiSP',
    'recipient': 'BM-2cVpswZo8rWLXDVtZEUNcDQvnvHJ6TLRYr',
    'sender': 'BM-2cVpswZo8rWLXDVtZEUNcDQvnvHJ6TLRYr'
}


class AddressBook(TeleniumTestProcess):
    """AddressBook Screen Functionality Testing"""
    test_label = 'Auto Responder'
    test_subject = 'Test Subject'
    test_body = 'Hey,This is draft Message Body from Address Book'

    @skip_screen_checks
    @ordered
    def test_save_address(self):
        """Saving a new Address On Address Book Screen/Window"""
        # Checking current Screen(Inbox screen)
        self.assert_wait_no_except('//ScreenManager[@current]', timeout=15, value='inbox')
        # This is for checking the Side nav Bar is closed
        self.assertExists('//MDNavigationDrawer[@status~=\"closed\"]', timeout=5)
        # This is for checking the menu button is appeared
        self.assertExists('//MDActionTopAppBarButton[@icon~=\"menu\"]', timeout=5)
        # This is for opening Nav drawer
        self.cli.wait_click('//MDActionTopAppBarButton[@icon=\"menu\"]', timeout=5)
        # checking state of Nav drawer
        self.assertExists("//MDNavigationDrawer[@state~=\"open\"]", timeout=5)
        # this is for scrolling Nav drawer
        self.drag("//NavigationItem[@text=\"Sent\"]", "//NavigationItem[@text=\"Inbox\"]")
        # assert for checking scroll function
        self.assertCheckScrollDown('//ContentNavigationDrawer//ScrollView[0]', timeout=5)
        # this is for opening setting screen
        self.cli.wait_click('//NavigationItem[@text=\"Address Book\"]', timeout=5)
        # Checking current screen
        self.assertExists("//ScreenManager[@current=\"addressbook\"]", timeout=5)
        # This is for checking the Side nav Bar is closed
        self.assertExists('//MDNavigationDrawer[@status~=\"closed\"]', timeout=5)
        # Check for rendered button
        self.assertExists('//MDActionTopAppBarButton[@icon=\"account-plus\"]', timeout=5)
        # Click on "Account-Plus' Icon to open popup to save a new Address
        self.cli.wait_click('//MDActionTopAppBarButton[@icon=\"account-plus\"]', timeout=5)
        # Checking the Label Field shows Validation for empty string
        self.assertExists('//GrashofPopup/BoxLayout[0]/MDTextField[@hint_text=\"Label\"][@text=\"\"]', timeout=5)
        # Checking the Address Field shows Validation for empty string
        self.assertExists('//GrashofPopup/BoxLayout[0]/MDTextField[@hint_text=\"Address\"][@text=\"\"]', timeout=5)
        # Click On save Button to check Field validation
        self.cli.wait_click('//MDRaisedButton[@text=\"Save\"]', timeout=5)
        # Add an address Label to label Field
        self.cli.setattr('//GrashofPopup/BoxLayout[0]/MDTextField[@hint_text=\"Label\"]', 'text', self.test_label)
        # Checking the Label Field should not be empty
        self.assertEqual(
            self.cli.getattr('//GrashofPopup/BoxLayout[0]/MDTextField[0][@text]', 'text'), self.test_label)
        # Add incorrect Address to Address Field to check validation
        self.cli.setattr(
            '//GrashofPopup/BoxLayout[0]/MDTextField[@hint_text=\"Address\"]',
            'text', test_address['invalid_address'])
        # Checking the Address Field should not be empty
        self.assertEqual(
            self.cli.getattr('//GrashofPopup/BoxLayout[0]/MDTextField[1][@text]', 'text'),
            test_address['invalid_address'])
        # Add Correct Address
        self.cli.setattr(
            '//GrashofPopup/BoxLayout[0]/MDTextField[@hint_text=\"Address\"]', 'text',
            test_address['autoresponder_address'])
        # Checking the Address Field contains correct address
        self.assertEqual(
            self.cli.getattr('//GrashofPopup/BoxLayout[0]/MDTextField[1][@text]', 'text'),
            test_address['autoresponder_address'])
        # Click on Save Button to save the address in address book
        self.cli.wait_click('//MDRaisedButton[@text=\"Save\"]', timeout=2)
        # Validating the Label field
        self.assertExists('//GrashofPopup/BoxLayout[0]/MDTextField[0][@text=\"Auto Responder\"]', timeout=3)
        # Validating the Valid Address is entered
        self.assertExists(
            '//GrashofPopup/BoxLayout[0]/MDTextField[1][@text=\"BM-2cVWtdUzPwF7UNGDrZftWuHWiJ6xxBpiSP\"]', timeout=3)
        # Check Current Screen (Address Book)
        self.assertExists("//ScreenManager[@current=\"addressbook\"]", timeout=5)
        # Checking new address should be added
        self.assertExists('//SwipeToDeleteItem', timeout=5)

    @skip_screen_checks
    @ordered
    def test_dismiss_addressbook_popup(self):
        """This method is to perform Dismiss add Address popup"""
        # Checking the "Address saving" Popup is not opened
        self.assertNotExists('//GrashofPopup', timeout=5)
        # Checking the "Add account" Button is rendered
        self.assertExists('//MDActionTopAppBarButton[@icon=\"account-plus\"]', timeout=6)
        # Click on Account-Plus Icon to open popup for add Address
        self.cli.wait_click('//MDActionTopAppBarButton[@icon=\"account-plus\"]', timeout=5)
        # Add Label to label Field
        self.cli.setattr('//GrashofPopup/BoxLayout[0]/MDTextField[0]', 'text', 'test_label2')
        # Checking the Label Field should not be empty
        self.assertNotEqual('//GrashofPopup/BoxLayout[0]/MDTextField[@hint_text=\"Label\"]', '')
        # Add Address to Address Field
        self.cli.setattr('//GrashofPopup/BoxLayout[0]/MDTextField[1]', 'text', test_address['recipient'])
        # Checking the Address Field should not be empty
        self.assertNotEqual('//GrashofPopup/BoxLayout[0]/MDTextField[@hint_text=\"Address\"]', '')
        # Checking for "Cancel" button is rendered
        self.assertExists('//MDRaisedButton[@text=\"Cancel\"]', timeout=5)
        # Click on 'Cancel' Button to dismiss the popup
        self.cli.wait_click('//MDRaisedButton[@text=\"Cancel\"]', timeout=2)
        # Check Current Screen (Address Book)
        self.assertExists("//ScreenManager[@current=\"addressbook\"]", timeout=5)

    @skip_screen_checks
    @ordered
    def test_send_message_to_saved_address(self):
        """This method is to send msg to the saved address from addressbook"""
        # Checking the Message detail Dialog box is not opened
        self.assertNotExists('//MDDialog', timeout=3)
        # Checking the saved address is rendered
        self.assertExists('//AddressBook/BoxLayout[0]//SwipeToDeleteItem[0]', timeout=5)
        # Click on a Address to open address Details popup
        self.cli.wait_click('//AddressBook/BoxLayout[0]//SwipeToDeleteItem[0]', timeout=5)
        # Checking the Message detail Dialog is opened
        self.assertExists('//MDDialog', timeout=3)
        # Checking the buttons are rendered
        self.assertExists('//MDRaisedButton', timeout=5)
        # Click on the Send to message Button
        self.cli.wait_click('//MDRaisedButton[0]', timeout=5)
        # Redirected to message composer screen(create)
        self.assertExists("//ScreenManager[@current=\"create\"]", timeout=5)
        # Checking the Address is populated to recipient field when we try to send message to saved address.
        self.assertExists(
            '//DropDownWidget/ScrollView[0]//MyTextInput[@text="BM-2cVWtdUzPwF7UNGDrZftWuHWiJ6xxBpiSP"]', timeout=5)