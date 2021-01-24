import PyPDF2


def confirm_meeting_date():
    pass


def create_dateframes():
    meetings = pd.DataFrame(
        columns=["date", "president", "mayor", "no_of_protests", "no_of_settlements"]
    )
    return meetings


def parse_long_dates(string):
    year = string[-4:]
    month = string[:3]
    try:
        month = str(time.strptime(month, "%b").tm_mon)
    except ValueError as err:
        print(f"Encountered ValueError on file: {string}")
    day = string.split(" ")[1]
    day = "".join(filter(str.isdigit, day))
    return year, month, day


def read_pdfs(path):
    pdf_paths = list(pdf_dir.rglob("*.pdf"))
    text_df = pd.DataFrame()
    for pdf_path in pdf_paths:
        print(pdf_path)
        minutes = ""
        pdfFileObj = open(pdf_path, "rb")
        try:
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        except:
            print(f"An error occurred reading file {pdf_path}")
        for idx, page in enumerate(pdfReader.pages):
            if idx == 0:
                first_page = page.extractText()
            else:
                minutes += page.extractText()
        date_search = re.findall(
            r"(?<=ESTIMATES)(.*?)(?=\s*MINUTES)", minutes.replace("\n", " ")
        )
        if date_search:
            # import pdb; pdb.set_trace()
            date_string = date_search[0].strip()
            if date_string[0].isalpha():
                print(f"Found a long date: {date_string}")
                pdf_year, pdf_month, pdf_day = parse_long_dates(date_string)
                date_string = "/".join([pdf_month, pdf_day, pdf_year])

            else:
                date_string = date_string.replace(" ", "")

            print(f"Date string!: {date_string}")
            try:
                date = datetime.strptime(date_string, "%m/%d/%Y").date()
            except ValueError:
                try:
                    date = datetime.strptime(date_string, "%m/%d/%y").date()
                except ValueError as err:
                    print(f"An error occurred with file {pdf_path}: {err}")
            row = {"date": date, "first_page": first_page, "minutes": minutes}
            text_df = text_df.append(row, ignore_index=True)
            print(len(text_df))
        else:
            # import pdb; pdb.set_trace()
            print(f"No date found in file {pdf_path}")


root = Path.cwd()
pdf_dir = root / "pdf_files"

read_pdfs(pdf_dir)
