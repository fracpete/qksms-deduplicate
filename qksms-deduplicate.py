import argparse
import json
import traceback


def deduplicate(input_file, output_file):
    """
    Deduplicates the messages:

    :param input_file: the JSON file to read from
    :type input_file: str
    :param output_file: the JSON file to write the cleaned up messages to
    :type output_file: str
    """
    with open(input_file, "r") as fp:
        input_data = json.load(fp)

    message_count = 0
    duplicate_count = 0
    output_data = {
        "messageCount": 0,
        "messages": list(),
    }
    message_dates = set()
    for message in input_data["messages"]:
        if message["date"] not in message_dates:
            message_dates.add(message["date"])
            output_data["messages"].append(message)
            message_count += 1
        else:
            duplicate_count += 1

    output_data["messageCount"] = message_count
    with open(output_file, "w") as fp:
        json.dump(output_data, fp, indent='\t', ensure_ascii=False)

    print("Input messages: %d" % input_data["messageCount"])
    print("Duplicate messages: %d" % duplicate_count)
    print("Output messages: %d" % message_count)


def main(args=None):
    """
    Performs the deduplication.
    Use -h to see all options.

    :param args: the command-line arguments to use, uses sys.argv if None
    :type args: list
    """

    parser = argparse.ArgumentParser(
        description='Deduplicates a QKSMS Backup JSON archive.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--input", metavar="FILE", required=True, help="The JSON file to process.")
    parser.add_argument("-o", "--output", metavar="FILE", required=True, help="The JSON file to save the deduplicate data to.")
    parsed = parser.parse_args(args=args)
    deduplicate(parsed.input, parsed.output)


def sys_main():
    """
    Runs the main function using the system cli arguments, and
    returns a system error code.

    :return: 0 for success, 1 for failure.
    :rtype: int
    """

    try:
        main()
        return 0
    except Exception:
        print(traceback.format_exc())
        return 1


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(traceback.format_exc())

