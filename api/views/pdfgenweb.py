import pdfkit
pdf = pdfkit.from_url('http://google.com', False)
with open('applicant_name.pdf', 'wb') as f:
        f.write(pdf)