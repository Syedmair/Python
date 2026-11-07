### Q5. Notification Dispatcher | Beginner
### Create EmailNotification, SMSNotification, and PushNotification classes. Each must implement send(message) with output specific to its channel. Write a single function notify_all(notifications, message) that iterates through different notification objects and invokes send(). Add a WhatsAppNotification class without changing the dispatcher. Explain where polymorphism occurs.
### ```[cite: 13]

class EmailNotification:

    def send(self, msg: str) -> None:
        print(f"Sending Email: {msg}")


class SMSNotification:

    def send(self, msg: str) -> None:
        print(f"Sending SMS: {msg}")


class PushNotification:

    def send(self, msg: str) -> None:
        print(f"Sending Push Notification: {msg}")


class WhatsAppNotification:

    def send(self, msg: str) -> None:
        print(f"Sending WhatsApp: {msg}")


def notify_all(notifs: list, msg: str) -> None:
    for notification in notifs:
        notification.send(msg)


if __name__ == "__main__":
    notification_list = [
        EmailNotification(),
        SMSNotification(),
        PushNotification(),
        WhatsAppNotification(),
    ]
    notify_all(notification_list, "Assignment reminder!")