import pandas as pd

GROUP1 = ['HIN A LIT', 'GER A LIT', 'SPA A LIT', 'KOR A LIT', 'GER A', 'CHI A1', 'ENG A1', 'IND A1', 'KOR A1', 'HIN A1', 'SWE A1', 'JAP A LIT', 'CHI A L&L', 'CHI A LIT', 'ENG A LIT', 'ENG A L&L']
GROUP2 = ['CHI B', 'FRE B', 'CHI A2', 'ENG A2', 'MAN B', 'MAN ABIN', 'SPA ABIN', 'SPA B', 'FRE ABIN', 'MAN ABIN']
GROUP3 = ['B&M', 'ECO', 'GEO', 'HIS', 'PSY', 'FIL', 'ITG', 'PHI']
GROUP4 = ['ESS', 'BIO', 'CHE', 'PHY', 'D&T', 'SPO SCI']
GROUP5 = ['MAT', 'MAT STUD']
GROUP6 = ['THE', 'VIA', 'MUS']

DFORIGINAL = pd.read_csv('assets/rchk_exam_data.csv')

ROW_MARGIN = '20px'
BOTTOM_MARGIN = '50px'
PAD_TABLE = '20px'
