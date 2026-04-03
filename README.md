## Cara Menjalankan Secara Lokal

### 1. Clone repository
```bash
git clone <URL_REPOSITORY>
cd <NAMA_FOLDER_PROJECT>
```

### 2. Buat dan aktifkan virtual environment

Windows
```bash
python -m venv env
env\Scripts\activate
```

MacOS / Linux
```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install dependency
```bash
pip install -r requirements.txt
```

### 4. Buat file .env di root project, lalu isi dengan format berikut:
```env 
PRODUCTION=False

GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback/
GROUP_MEMBERS=rayyan.emir@ui.ac.id,angga.tri41@ui.ac.id,philo.pradipta41@ui.ac.id,raihan.maulana41@ui.ac.id,zakiy.nashrudin@ui.ac.id,contoh@gmail.com,contohlagi@gmail.com
```

## Keterangan
- contoh@gmail.com dan contohlagi@gmail.com hanya berupa contoh dan dapat diganti dengan email tester jika pengujian fitur ingin dilakukan.
- Jika aplikasi dijalankan di `http://localhost:8000`, gunakan:
  `GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback/`
- Jika aplikasi dijalankan di `http://127.0.0.1:8000`, gunakan:
  `GOOGLE_REDIRECT_URI=http://127.0.0.1:8000/auth/callback/`

### 5. Jalankan migrasi database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Jalankan server
```bash
python manage.py runserver
```

### 7. Buka di browser
```txt
http://localhost:8000
```
### Alternatif 
```txt
http://127.0.0.1:8000
```

## Catatan
- Credential asli tidak disertakan di repository publik.
- Credential testing diberikan secara privat pada berkas submission.
- Jika OAuth Google masih dalam mode testing, email penguji harus ditambahkan ke daftar **Test Users** agar login dapat berhasil.