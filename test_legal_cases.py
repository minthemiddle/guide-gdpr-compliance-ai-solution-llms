import unittest
from main import anonymize_text, de_anonymize_text, client

class TestLegalCases(unittest.TestCase):
    def process_case(self, case):
        anonymized_case, pii_map = anonymize_text(case)
        completion = client.beta.chat.completions.parse(
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
        ],
        (
            "In a shocking turn of events, renowned scientist Dr. Elena Vasquez (born 02/15/1972) has filed a groundbreaking lawsuit against her former employer, BioTech Innovations. The case, initiated on September 3, 2024, alleges severe ethical violations in genetic research. Dr. Vasquez, contactable at evasquez@email.com or +1 650 555 1111, resides at 789 Redwood Lane, Palo Alto, CA 94301. Her NIH ID is NIH1234567.",
            "• Dr. Elena Vasquez filed a lawsuit against BioTech Innovations on September 3, 2024\n• The case alleges severe ethical violations in genetic research\n• Dr. Vasquez was born on 02/15/1972\n• She resides in Palo Alto, California"
        ),
        (
            "A class-action lawsuit has been brought against Fast Food Chain X by lead plaintiff Samuel Johnson (DOB: 11/30/1995). Filed on July 15, 2024, the suit claims widespread food safety violations across multiple states. Johnson, a resident of 456 Elm St, Chicago, IL 60601 (phone: 312-555-7890, email: s.johnson@email.com), is represented by the law firm Smith & Associates. His Illinois Food Handler Certificate number is IL-FH-98765.",
            "• Samuel Johnson filed a class-action lawsuit against Fast Food Chain X on July 15, 2024\n• The suit claims widespread food safety violations across multiple states\n• Samuel Johnson was born on 11/30/1995\n• He resides in Chicago, Illinois"
        ),
        (
            "Environmental activist group EarthFirst, led by Maya Patel (DOB 09/22/1988), has initiated legal proceedings against OilCorp International for alleged violations of the Clean Air Act. The lawsuit, filed in federal court on October 10, 2024, seeks substantial penalties and immediate corrective action. Patel, residing at 123 Green St, Portland, OR 97201, can be reached at 503-555-2468 or maya.p@earthfirst.org. Her Oregon Environmental Leadership ID is OR-EL-654321.",
            "• Environmental activist group EarthFirst, led by Maya Patel, initiated legal proceedings against OilCorp International on October 10, 2024\n• The lawsuit alleges violations of the Clean Air Act\n• Maya Patel was born on 09/22/1988\n• She resides in Portland, Oregon"
        ),
        (
            "Former CEO Richard Blackstone is facing a complex securities fraud case. The Securities and Exchange Commission filed charges on December 5, 2024, alleging insider trading and market manipulation during his tenure at MegaCorp Ltd. Blackstone, born 07/04/1965, resides in a penthouse at 1000 Park Avenue, New York, NY 10028. His attorney can be reached at 212-555-9999. Blackstone's SEC filing number is SEC-RB-789012.",
            "• The Securities and Exchange Commission filed charges against former CEO Richard Blackstone on December 5, 2024\n• The case alleges insider trading and market manipulation at MegaCorp Ltd\n• Richard Blackstone was born on 07/04/1965\n• He resides in New York City"
        ),
        (
            "A landmark digital privacy case has been initiated by tech expert Aisha Rahman (born 03/18/1991) against social media giant ConnectMe. Filed on November 20, 2024, the lawsuit accuses ConnectMe of massive data breaches and illegal user profiling. Rahman, a cybersecurity consultant residing at 567 Tech Terrace, San Francisco, CA 94105, can be contacted through her legal team at privacy@techlaw.com. Her California Digital Privacy Advocate ID is CDPA-AR-135790.",
            "• Aisha Rahman filed a lawsuit against social media giant ConnectMe on November 20, 2024\n• The case accuses ConnectMe of massive data breaches and illegal user profiling\n• Aisha Rahman was born on 03/18/1991\n• She resides in San Francisco, California"
        ),
        (
            "In a surprising move, small business owner Jake Martinez has taken on e-commerce behemoth MegaShop in an antitrust lawsuit. Martinez, proprietor of Local Goods Emporium (Business ID: LGE-5678), alleges unfair competition and monopolistic practices. The case was filed on August 8, 2024. Martinez (DOB: 06/12/1980) operates from 789 Main Street, Austin, TX 78701, and can be reached at 512-555-3456 or jake@localgoodsemporium.com.",
            "• Jake Martinez filed an antitrust lawsuit against MegaShop on August 8, 2024\n• The case alleges unfair competition and monopolistic practices\n• Jake Martinez was born on 06/12/1980\n• He operates a small business in Austin, Texas"
        ),
        (
            "A group of former employees, led by software engineer Liam O'Connor (born 12/05/1987), has brought a class-action lawsuit against TechStart Inc., citing labor law violations and discriminatory practices. The suit, filed on January 15, 2025, represents over 500 affected individuals. O'Connor, residing at 234 Coder's Lane, Seattle, WA 98101, can be contacted at liam.oconnor@techworkers.org or 206-555-8765. His Washington State Bar Association number for the case is WSBA-98765.",
            "• Liam O'Connor led a class-action lawsuit against TechStart Inc., filed on January 15, 2025\n• The suit cites labor law violations and discriminatory practices\n• Liam O'Connor was born on 12/05/1987\n• He resides in Seattle, Washington"
        ),
        (
            "Renowned author J.K. Rowling (born 07/31/1965) has initiated a copyright infringement lawsuit against fanfiction website FanTales. The case, filed on March 3, 2025, alleges unauthorized commercial use of her characters and storylines. Rowling, represented by literary agency Bloomsbury & Associates, can be reached through her publicist at pr@jkrowling.com. Her UK Copyright Registration number is UKCR-789012.",
            "• J.K. Rowling filed a copyright infringement lawsuit against FanTales on March 3, 2025\n• The case alleges unauthorized commercial use of her characters and storylines\n• J.K. Rowling was born on 07/31/1965\n• She is represented by Bloomsbury & Associates"
        ),
        (
            "In a groundbreaking case, AI researcher Dr. Alan Turing (a pseudonym, real name withheld for privacy) has filed a lawsuit against RoboTech Corporation, challenging the company's claim of achieving artificial general intelligence (AGI). The suit, lodged on April 1, 2025, demands scientific proof and transparency. Dr. Turing, affiliated with the Institute for Ethical AI (ID: IEAI-246810), can be contacted via secure channels at whistleblower@ethicalai.org.",
            "• An AI researcher using the pseudonym Dr. Alan Turing filed a lawsuit against RoboTech Corporation on April 1, 2025\n• The case challenges RoboTech's claim of achieving artificial general intelligence\n• The plaintiff's real name is withheld for privacy\n• He is affiliated with the Institute for Ethical AI"
        ),
        (
            "Celebrity chef Gordon Ramsay has taken legal action against restaurant review app TasteBud for alleged defamation and manipulation of ratings. The lawsuit, filed on May 20, 2025, claims the app deliberately lowered ratings for Ramsay's restaurants. Ramsay, born 11/08/1966, owns multiple restaurants including the flagship at 10 Royal Hospital Road, London, SW3 4HP, UK. His legal team can be reached at legal@gordonramsay.com or +44 20 7352 4441. Ramsay's UK Business ID is UKBI-GR789012.",
            "• Gordon Ramsay filed a lawsuit against restaurant review app TasteBud on May 20, 2025\n• The case alleges defamation and manipulation of ratings\n• Gordon Ramsay was born on 11/08/1966\n• He owns multiple restaurants, including a flagship in London"
        )
        ]

        for i, (case, expected_summary) in enumerate(cases, 1):
            with self.subTest(f"Case {i}"):
                final_summary = self.process_case(case)
                self.assertEqual(final_summary.strip(), expected_summary.strip())

if __name__ == '__main__':
    unittest.main()
