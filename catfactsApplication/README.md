# Cat Facts Application

Bu proje, Cat Facts API'sinden kedi bilgileri (cat facts) çekip, bu verileri SQLite veritabanında saklayan ve çeşitli görselleştirmeler oluşturan bir Python uygulamasıdır. Uygulama, elde edilen verileri analiz eder ve kullanıcıya sunar.

## Proje İçeriği

Bu uygulama, aşağıdaki adımları içerir:

1. **API İsteği**: "https://cat-fact.herokuapp.com/facts" adresindeki API'ye bir GET isteği göndererek kedi bilgilerini alır.
2. **Veritabanı Oluşturma**: Alınan veriyi saklamak için bir SQLite veritabanı oluşturur. Bu veritabanında, kedi bilgilerini saklayacak bir tablo bulunur.
3. **Veri Kaydetme**: API'den alınan kedi bilgilerini SQLite veritabanına kaydeder.
4. **Veri Görselleştirme**: Veritabanına kaydedilen kedi bilgilerini analiz eder ve çeşitli grafiklerle görselleştirir.

## Kullanılan Teknolojiler

- **Python**: Proje geliştirilmesi için kullanılan programlama dili.
- **SQLite**: Veritabanı yönetim sistemi olarak kullanılmıştır.
- **Plotly Express**: Veri görselleştirmesi için kullanılmıştır.
- **WordCloud**: Kelime bulutu oluşturma aracı.

## Kurulum ve Kullanım

### Gereksinimler

- **Python 3.x**: En son Python sürümünü kullanmanız önerilir.
- **Gerekli Python Kütüphaneleri**: Aşağıdaki kütüphaneler kullanılmaktadır:
  - `requests`: HTTP istekleri göndermek için kullanılır.
  - `pandas`: Veri işleme ve analiz için kullanılır.
  - `sqlite3`: SQLite veritabanı ile etkileşim için kullanılır.
  - `plotly`: Veri görselleştirmesi için kullanılır.
  - `wordcloud`: Kelime bulutu oluşturmak için kullanılır.

### Adımlar

1. **Proje Deposu**: Bu projeyi yerel makinenize klonlayın.
   ```
   git clone https://github.com/USERNAME/UP-School-AI-First-Developer.git
   cd catfacts_Application
   ```

### Kullanım

1. **API'den Veri Çekme**:
   Uygulama, "https://cat-fact.herokuapp.com/facts" adresindeki API'den kedi bilgilerini çeker. Bu veriler JSON formatında gelir ve daha sonra işlenir.

2. **Veritabanına Kaydetme**:
   Çekilen veriler, SQLite veritabanında saklanır. Bu veritabanı, her bir kedi bilgisi için benzersiz bir ID, bilgi metni ve oluşturulma tarihini içeren bir tabloya sahiptir.

3. **Veri Görselleştirme**:
   - **Histogram**: Kedi bilgilerinin oluşturulma tarihlerine göre dağılımını gösterir.
   - **Bar Grafik**: Kedi bilgilerinin metin uzunluklarının dağılımını gösterir.
   - **Scatter Plot**: Metin uzunluğu ve kullanıcı ID'si arasındaki ilişkiyi gösterir.
   - **Kelime Sıklığı Histogramı**: En sık kullanılan kelimeleri gösterir.
   - **Kelime Bulutu**: Kedi bilgilerinde en çok geçen kelimeleri vurgulayan bir kelime bulutu oluşturur.

## Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasını inceleyebilirsiniz.
