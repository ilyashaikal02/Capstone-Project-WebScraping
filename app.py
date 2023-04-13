from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests
import time

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this


#1
#insert the scrapping here
#find your right key here
temp_new = [] # tuple (untuk menampung hasil akhir data yang dikeluarkan)

# Melakukan loop untuk 15 halaman pertama
for page_num in range(1, 16):
    
    # Mengirim permintaan GET ke website dan mem-parse konten HTML
    url = f'https://www.kalibrr.id/id-ID/job-board/te/data/{page_num}'
    response = requests.get(url)
    soup2 = BeautifulSoup(response.content, 'html.parser')

    # Mencari 15 elemen div dengan class 'class-div' pada halaman tersebut
    Title = soup2.find_all('div', {'class': 'k-col-start-3 k-row-start-1'})[:15]
    
    # Mencari 15 elemen span dengan class 'class-span' pada halaman tersebut
    Company = soup2.find_all('span', {'class': 'k-inline-flex k-items-center k-mb-1'})[:15]
    
      # Mencari 15 elemen span dengan class 'class-div' pada halaman tersebut
    Lokasi = soup2.find_all('div', {'class': 'k-flex k-flex-col md:k-flex-row'})[:15]
    
      # Mencari 15 elemen span dengan class 'class-span' pada halaman tersebut
    Date_work_and_submit = soup2.find_all('span', {'class': 'k-block k-mb-1'})[:15]

    # Menampilkan teks dari 15 elemen div yang ditemukan pada halaman tersebut
    for div_element in Title:
        print(div_element.text.strip())

    # Menampilkan teks dari 15 elemen span yang ditemukan pada halaman tersebut
    for span_element in Company:
        print(span_element.text.strip())
        
        # Menampilkan teks dari 15 elemen span yang ditemukan pada halaman tersebut
    for div_element2 in Lokasi:
        print(div_element2.text.strip())
        
        # Menampilkan teks dari 15 elemen span yang ditemukan pada halaman tersebut
    for span_element2 in Date_work_and_submit:
        print(span_element2.text.strip())

    # Memberikan jeda selama 1 detik sebelum melanjutkan ke halaman selanjutnya
    time.sleep(1)
    
    # Menambahkan data yang telah di looping secara otomatis (dengan append) ke masing2 variabel
    temp_new.append((Title, Company, Lokasi, Date_work_and_submit)) 

# Menambahkan len agar code html tidak muncul setelah looping selesai
print(len(temp_new))


#2
#Ekstraksi data
# proses ekstraksi data dari variabel "temp_new"

data = []
for page_data in temp_new:
    
    #1 Mengekstrak list yang telah dibuat dalam looping sebelumnya menjadi informasi text
    title_new = [Title.text.strip() for Title in page_data[0]]
    companies_new = [Company.text.strip() for Company in page_data[1]]
    location_new = [Lokasi.text.strip() for Lokasi in page_data[2]]
    DateWorkSubmit_new = [Date_work_and_submit.text.strip() for Date_work_and_submit in page_data[3]]
    
    #2 Menambahkan list yang baru saja dibentuk dengan operator penambahan list (+=) dan menggabungkannya dengan list(zip())
    data += list(zip(title_new, companies_new, location_new, DateWorkSubmit_new))


    #3
#change into dataframe
df_new = pd.DataFrame(data, columns=['Title', 'Company', 'Lokasi', 'Date_work_and_submit'])

#insert data wrangling here
df_new['Kota'] = df_new['Lokasi'].str.split(' · ').str[0]
df_new = df_new.drop('Lokasi', axis=1)
df_new['Date_work_post'] = df_new['Date_work_and_submit'].str.split(' • ').str[0]
df_new['Deadline_work_submit'] = df_new['Date_work_and_submit'].str.split(' • ').str[1]
df_new = df_new.drop('Date_work_and_submit', axis=1)

job_counts = df_new[['Kota']].value_counts()

#end of data wranggling

@app.route("/")
def index(): 
	
	card_data = f'{job_counts.mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = job_counts.sort_values(ascending=True).plot(figsize=(20,9));
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)