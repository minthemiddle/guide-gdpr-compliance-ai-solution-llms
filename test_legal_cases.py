import unittest
from main import anonymize_text, de_anonymize_text
from openai import OpenAI

class TestLegalCases(unittest.TestCase):
    def setUp(self):
        self.client = OpenAI()

    def process_case(self, case):
        anonymized_case, pii_map = anonymize_text(case)
        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Summarize this legal case in very short bullet points. Keep placeholders intact."},
                {"role": "user", "content": anonymized_case},
            ],
            response_format={"type": "json_object"},
        )
        summary = completion.choices[0].message.parsed["summary"]
        final_summary = de_anonymize_text(summary, pii_map)
        return final_summary

    def test_cases(self):
        cases = [
            (
                "On 5th April 2023, Sarah Johnson, born on 15/08/1990, filed a wrongful termination lawsuit against ABC Industries. The plaintiff, residing at 456 Oak Ave, New York, can be reached at +1 212 555 1234 or sarah.j@email.com. Her SSN is 123-45-6789. The case alleges discrimination based on gender.",
                "• Sarah Johnson filed a wrongful termination lawsuit against ABC Industries on 5th April 2023\n• The case alleges gender discrimination\n• Sarah Johnson was born on 15/08/1990\n• She resides in New York"
            ),
            (
                "Michael Brown, DOB 22/11/1978, initiated legal proceedings on 10th June 2023 against Global Tech Solutions. The complainant, living at 789 Pine St, San Francisco, is contactable at 415-555-6789 or m.brown@email.com. His California Driver's License number is Y1234567. The lawsuit claims unpaid overtime and violation of labor laws.",
                "• Michael Brown initiated legal proceedings against Global Tech Solutions on 10th June 2023\n• The lawsuit claims unpaid overtime and violation of labor laws\n• Michael Brown was born on 22/11/1978\n• He resides in San Francisco"
            ),
            (
                "On 20th July 2023, Emma Wilson (born 03/02/1995) filed a sexual harassment complaint against her former employer, XYZ Corporation. Emma, residing at 101 Elm Street, Chicago, can be contacted at +1 312 555 9876 or ewilson@email.com. Her Illinois State ID is IL-123-456-789. The case details multiple incidents of inappropriate behavior by her supervisor.",
                "• Emma Wilson filed a sexual harassment complaint against XYZ Corporation on 20th July 2023\n• The case involves multiple incidents of inappropriate behavior by her supervisor\n• Emma Wilson was born on 03/02/1995\n• She resides in Chicago"
            ),
            (
                "David Lee, born on 07/09/1982, initiated a class-action lawsuit on 15th August 2023 against Big Pharma Inc. The lead plaintiff, residing at 222 Maple Dr, Boston, can be reached at 617-555-3456 or d.lee@email.com. His passport number is 98765432. The lawsuit alleges false advertising and harmful side effects of a popular medication.",
                "• David Lee initiated a class-action lawsuit against Big Pharma Inc on 15th August 2023\n• The lawsuit alleges false advertising and harmful side effects of a popular medication\n• David Lee was born on 07/09/1982\n• He resides in Boston"
            ),
            (
                "On 1st September 2023, Maria Rodriguez (DOB: 12/04/1988) filed a workplace injury claim against Construction Co. Ltd. Maria, living at 333 Cedar Lane, Miami, is reachable at +1 305 555 7890 or m.rodriguez@email.com. Her Florida ID number is F123-456-78-910-0. The case involves a severe injury sustained on a construction site due to alleged safety violations.",
                "• Maria Rodriguez filed a workplace injury claim against Construction Co. Ltd on 1st September 2023\n• The case involves a severe injury sustained on a construction site due to alleged safety violations\n• Maria Rodriguez was born on 12/04/1988\n• She resides in Miami"
            ),
            (
                "Alex Thompson, born 30/06/1993, initiated legal action on 10th October 2023 against Tech Giant Corporation for patent infringement. Alex, residing at 444 Birch Street, Seattle, can be contacted at 206-555-2345 or a.thompson@email.com. Their Washington State ID is WDL-123-456-789. The lawsuit claims unauthorized use of a proprietary software algorithm.",
                "• Alex Thompson initiated legal action against Tech Giant Corporation for patent infringement on 10th October 2023\n• The lawsuit claims unauthorized use of a proprietary software algorithm\n• Alex Thompson was born on 30/06/1993\n• They reside in Seattle"
            ),
            (
                "On 15th November 2023, Jennifer Patel (DOB: 18/07/1986) filed a discrimination lawsuit against Mega Retail Inc. Jennifer, living at 555 Willow Ave, Houston, is reachable at +1 713 555 6789 or j.patel@email.com. Her Texas Driver's License number is 12345678. The case alleges racial discrimination in promotion practices.",
                "• Jennifer Patel filed a discrimination lawsuit against Mega Retail Inc on 15th November 2023\n• The case alleges racial discrimination in promotion practices\n• Jennifer Patel was born on 18/07/1986\n• She resides in Houston"
            ),
            (
                "Robert Chen, born on 25/03/1979, initiated a whistleblower lawsuit on 5th December 2023 against Finance Corp. Robert, residing at 666 Oak Street, Los Angeles, can be reached at 323-555-9876 or r.chen@email.com. His California ID is CA1234567. The lawsuit exposes alleged financial fraud and insider trading within the company.",
                "• Robert Chen initiated a whistleblower lawsuit against Finance Corp on 5th December 2023\n• The lawsuit exposes alleged financial fraud and insider trading within the company\n• Robert Chen was born on 25/03/1979\n• He resides in Los Angeles"
            ),
            (
                "On 20th January 2024, Olivia Foster (DOB: 09/10/1992) filed a breach of contract claim against Software Solutions LLC. Olivia, living at 777 Pine Lane, Denver, is contactable at +1 303 555 3456 or o.foster@email.com. Her Colorado State ID is CO-987-654-321. The case involves a dispute over software development project deliverables and payment terms.",
                "• Olivia Foster filed a breach of contract claim against Software Solutions LLC on 20th January 2024\n• The case involves a dispute over software development project deliverables and payment terms\n• Olivia Foster was born on 09/10/1992\n• She resides in Denver"
            ),
            (
                "James Wilson, born 14/12/1975, initiated legal proceedings on 8th February 2024 against Green Energy Co. for intellectual property theft. James, residing at 888 Elm Road, Portland, can be contacted at 503-555-7890 or j.wilson@email.com. His Oregon Driver's License number is OR123456. The lawsuit claims unauthorized use of a patented renewable energy technology.",
                "• James Wilson initiated legal proceedings against Green Energy Co. for intellectual property theft on 8th February 2024\n• The lawsuit claims unauthorized use of a patented renewable energy technology\n• James Wilson was born on 14/12/1975\n• He resides in Portland"
            ),
            (
                "On 1st March 2024, Sophia Kim (DOB: 27/05/1989) filed a class-action lawsuit against Food Processing Inc. Sophia, living at 999 Maple Street, Atlanta, is reachable at +1 404 555 2345 or s.kim@email.com. Her Georgia ID number is GA987654321. The case alleges widespread food contamination and failure to meet safety standards.",
                "• Sophia Kim filed a class-action lawsuit against Food Processing Inc on 1st March 2024\n• The case alleges widespread food contamination and failure to meet safety standards\n• Sophia Kim was born on 27/05/1989\n• She resides in Atlanta"
            ),
            (
                "Daniel Martinez, born on 03/08/1984, initiated a workplace harassment lawsuit on 15th April 2024 against Corporate Services Ltd. Daniel, residing at 111 Cedar Drive, Phoenix, can be reached at 602-555-6789 or d.martinez@email.com. His Arizona State ID is AZ-123-456-789. The lawsuit details a pattern of bullying and hostile work environment.",
                "• Daniel Martinez initiated a workplace harassment lawsuit against Corporate Services Ltd on 15th April 2024\n• The lawsuit details a pattern of bullying and hostile work environment\n• Daniel Martinez was born on 03/08/1984\n• He resides in Phoenix"
            ),
            (
                "On 10th May 2024, Emily Chang (DOB: 19/01/1991) filed an equal pay lawsuit against Media Group Inc. Emily, living at 222 Birch Avenue, Philadelphia, is contactable at +1 215 555 9876 or e.chang@email.com. Her Pennsylvania Driver's License number is PA98765432. The case claims gender-based pay discrimination in the workplace.",
                "• Emily Chang filed an equal pay lawsuit against Media Group Inc on 10th May 2024\n• The case claims gender-based pay discrimination in the workplace\n• Emily Chang was born on 19/01/1991\n• She resides in Philadelphia"
            ),
            (
                "Thomas Anderson, born 11/11/1980, initiated legal action on 20th June 2024 against AI Systems Corporation for privacy violations. Thomas, residing at 333 Willow Lane, Austin, can be contacted at 512-555-3456 or t.anderson@email.com. His Texas State ID is TX-987-654-321. The lawsuit alleges unauthorized collection and use of personal data.",
                "• Thomas Anderson initiated legal action against AI Systems Corporation for privacy violations on 20th June 2024\n• The lawsuit alleges unauthorized collection and use of personal data\n• Thomas Anderson was born on 11/11/1980\n• He resides in Austin"
            ),
            (
                "On 5th July 2024, Aisha Patel (DOB: 08/06/1987) filed a wrongful termination suit against Healthcare Solutions Inc. Aisha, living at 444 Oak Court, Dallas, is reachable at +1 214 555 7890 or a.patel@email.com. Her Texas Medical License number is TML123456. The case claims retaliation for reporting patient safety concerns.",
                "• Aisha Patel filed a wrongful termination suit against Healthcare Solutions Inc on 5th July 2024\n• The case claims retaliation for reporting patient safety concerns\n• Aisha Patel was born on 08/06/1987\n• She resides in Dallas"
            )
        ]

        for i, (case, expected_summary) in enumerate(cases, 1):
            with self.subTest(f"Case {i}"):
                final_summary = self.process_case(case)
                self.assertEqual(final_summary.strip(), expected_summary.strip())

if __name__ == '__main__':
    unittest.main()
