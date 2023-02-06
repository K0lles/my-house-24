from django.core.management.base import BaseCommand

from site_management.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        if MainPage.objects.all().count() == 0:
            main_page_seo = Seo.objects.create(
                title='Головна сторінка',
                description='Мой Дом 24, розташований в м.Одеса',
                keywords='Мой Дом 24, Головна сторінка, Квартири'
            )
            MainPage.objects.create(
                seo=main_page_seo,
                show_urls=True,
                slide_1='start_commands/site_management/main_page_slides/1.jpg',
                slide_2='start_commands/site_management/main_page_slides/2.jpg',
                slide_3='start_commands/site_management/main_page_slides/3.jpg',
                title='Головна сторінка сайту Мой Дом 24',
                short_text="<p>Житловий комплекс <strong>Nord</strong> розташований на <strong>Чорному морі</strong> в мальовничій зоні <strong>Одеси</strong>. Оригінальна архітектура комплексу робить його унікальним предметом не лише для Одеси, але й для всієї України - будинок ідеально вписується в архітектуру <strong>узбережжя</strong> і відкриває своїх жителів та гостей чудовим видом на нескінченне море. Яскравою перевагою житлового комплексу є його розташування - <i>зручна транспортна розв'язка, соціальна інфраструктура, парк та відмінне морське повітря</i> створюють усі умови для <i>комфортного проживання.</i></p>",
                block_header_1='Магазини, банки та школи',
                block_description_1="<p>Район розташування житлового комплексу має всю необхідну для проживання соціальну інфраструктуру – в безпосередній близькості знаходяться лікувально-профілактичні заклади, аптеки, магазини, відділення банків, приватні та комерційні дитячі садки, школи</p>",
                block_photo_1='start_commands/site_management/main_page_blocks/1.jpeg',
                block_header_2='Ресторани і кафе',
                block_description_2="<p>Неподалік від житлового комплексу розташований рибний ресторан та італійська піцерія. Крім того, всього за десять хвилин ходьби від комплексу знаходяться ресторани іспанської, італійської, американської, української та російської кухні, піцерії, кафе та лаунж-бари на будь-який смак.</p>",
                block_photo_2='start_commands/site_management/main_page_blocks/2.jpeg',
                block_header_3='Пляж',
                block_description_3="<p>Житловий комплекс розташований на березі Чорного моря у районі Аркадія. За десять хвилин ходьби від нього знаходяться знамениті пляжі Аркадія та Чайка, а трохи далі – пляжі курортний, 13-та станція Великого Фонтану, Пляжник та інші знамениті пляжі Одеси!</p>",
                block_photo_3='start_commands/site_management/main_page_blocks/3.jpeg',
                block_header_4='Спортивний комплекс',
                block_description_4="<p>Всього в 5 хвилинах ходьби від житлового комплексу знаходиться Спортивний комплекс Міжнародного гуманітарного університету – це сучасний обладнаний комплекс із залами для проведення волейбольних змагань, змагань з танців та боротьби та інших спортивних заходів!</p>",
                block_photo_4='start_commands/site_management/main_page_blocks/4.jpeg',
                block_header_5='Клубне життя',
                block_description_5="<p>Район розташування житлового комплексу Аркадія є культовим місцем нічного відпочинку та розваги – буквально за 5-10 хвилин ходьби від комплексу знаходяться такі місця зосередження клубного життя країни!</p>",
                block_photo_5='start_commands/site_management/main_page_blocks/5.jpeg',
                block_header_6="Зручна транспортна розв'язка",
                block_description_6="<p>ЖК розташована на березі Чорного моря в районі Аркадії і має зручну транспортну розв'язку, що дозволяє навіть за годину Пік швидко та без проблем доїхати протягом десяти хвилин до центру міста чи виїхати на автостради Одеської обл!</p>",
                block_photo_6='start_commands/site_management/main_page_blocks/6.jpeg'
            )

        if AboutUs.objects.all().count() == 0:
            about_us_seo = Seo.objects.create(
                title='Про нас',
                description='Мой Дом 24, розташований в м.Одеса',
                keywords='Мой Дом 24, Про нас, Квартири'
            )
            about_us_gallery = Gallery.objects.create(
                name='About Us gallery'
            )

            about_us_additional_gallery = Gallery.objects.create(
                name='Additional Gallery about us'
            )

            about_us = AboutUs.objects.create(
                gallery=about_us_gallery,
                additional_gallery=about_us_additional_gallery,
                seo=about_us_seo,
                title='Про нашу компанію',
                director_photo='start_commands/site_management/about_us/director_photo.jpeg',
                short_text="<p><strong>Компанія-забудовник</strong> не лише створила цей об'єкт для своїх покупців, а й після закінчення будівництва взяла на себе всі послуги із забезпечення зручного проживання своїх мешканців. Для цього було організовано керуючу компанію «Морська симфонія», яка здійснює комплексне обслуговування комунальної сфери життєдіяльності своїх клієнтів.</p><p>Місією компанії, що управляє, є така схема взаємодії з мешканцями будинку, при якій послуги компанії не відволікають їх від проживання та відпочинку і створюють максимально комфортну екосистему в будинку. Непомітний сервіс та максимально ефективна робота є візитною карткою компанії.</p><p><br>У функції <i>керуючої компанії входять як утримання</i> та управління господарством комплексу, так і охоронюваної прибудинкової території – прибирання, технічне обслуговування ліфтового господарства, системи електро та водопостачання будинку, котельні та пожежної системи, диспетчеризація, охорона, утримання прибудинкової території та багато іншого. У штаті компанії зібрано лише професіоналів своєї справи, які допоможуть мешканцям у найважчих та критичних ситуаціях вирішити їхні житлово-комунальні проблеми сім днів на тиждень цілодобово – електрики та сантехніки, інженери, монтери та інші фахівці мають багаторічний досвід та високий рівень кваліфікації.</p><p>Все це робить житловий комплекс унікальним, комфортним та безпечним місцем для проживання та відпочинку всієї родини цілий рік. Довірте турботу про ваш будинок і вашу квартиру <strong>керуючої компанії</strong> і ви зможете цілий рік насолоджуватися проживанням на березі моря та прекрасною природою Одеси.</p>",
                additional_title='Додатково про нас',
                additional_text="<p>Головним обов'язком керуючої компанії є підтримка комфортних умов для мешканців, оперативне реагування на їхні прохання та побажання</p><p><strong>Додаткові послуги керуючої компанії також належать: 24-годинна охорона прибудинкової території та паркінгу, прибирання території та вивіз сміття, обслуговування пірсу та пляжу. Також за бажання мешканці будинку можуть замовити будь-які будівельно-ремонтні роботи від штатної бригади компанії</strong></p>",
            )

            Photo.objects.create(
                gallery=about_us_gallery,
                photo='start_commands/site_management/about_us/gallery/1.jpg'
            )

            Document.objects.create(
                about_us=about_us,
                title='Перший документ',
                file='start_commands/site_management/about_us/documents/1.jpg'
            )

            Document.objects.create(
                about_us=about_us,
                title='Другий документ',
                file='start_commands/site_management/about_us/documents/2.jpg'
            )

        if ServiceFront.objects.all().count() == 0:
            service_seo = Seo.objects.create(
                title='Послуги Мой Дом 24',
                description='Мой Дом 24, розташований в м.Одеса',
                keywords='Мой Дом 24, Послуги, Квартири'
            )

            service_front = ServiceFront.objects.create(
                seo=service_seo
            )

            ServiceObjectFront.objects.create(
                service_front=service_front,
                photo='start_commands/site_management/about_us/services/1.jpeg',
                title='Встановлення систем безпеки',
                description="<p>Житловий комплекс має свій <strong>чотирирівневий надземний паркінг</strong>, обслуговування якого здійснює керуюча компанія.<br>Обслуговування паркінгу включає такі роботи та послуги: Прибирання території, <i>Підтримка функціонування </i>інженерних мереж паркінгу, Обслуговування системи виїзду-в'їзду в паркінг, Забезпечення функціонування пропускного режиму для в'їзду на територію паркінгу, Охорона та забезпечення безпеки мешканців та автомобільного транспорту.</p>"
            )

        if TariffPage.objects.all().count() == 0:
            tariff_seo = Seo.objects.create(
                title='Тарифи Мой Дом 24',
                description='Мой Дом 24, розташований в м.Одеса',
                keywords='Мой Дом 24, Тарифи, Квартири'
            )

            tariff = TariffPage.objects.create(
                title='Тарифи',
                short_text="<p><i><strong>Короткий текст тарифів</strong></i></p>",
                seo=tariff_seo
            )

            TariffObjectFront.objects.create(
                tariff_page=tariff,
                photo='start_commands/site_management/about_us/tariff_objects/1.jpg',
                title='Перший тариф'
            )

        if Contact.objects.all().count() == 0:
            contact_seo = Seo.objects.create(
                title='Контакти Мой Дом 24',
                description='Мой Дом 24, розташований в м.Одеса',
                keywords='Мой Дом 24, Контакти, Квартири'
            )

            Contact.objects.create(
                seo=contact_seo,
                title='Контакти',
                text="<p><strong>Компанія-забудовник</strong> не лише створила цей об'єкт для своїх покупців, а й після закінчення будівництва взяла на себе всі послуги із забезпечення зручного проживання своїх мешканців. Для цього було організовано керуючу компанію «Морська симфонія», яка здійснює комплексне обслуговування комунальної сфери життєдіяльності своїх клієнтів.</p>",
                commercial_url='https://avada-media.ua',
                name_surname_father='AVADA-MEDIA',
                location='вул. Космонавтів, 32',
                address='Малинівський р-н, м. Одеса',
                phone='+380999999999',
                email='info@avada-media.com.ua',
                map_code=f"<div class='map'><iframe src='https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2749.8611266486014!2d30.713265815873395!3d46.43163207638925!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x40c633a651e3fd09%3A0x9331380952bbfd2c!2z0LLRg9C70LjRhtGPINCa0L7RgdC80L7QvdCw0LLRgtGW0LIsIDMyLCDQntC00LXRgdCwLCDQntC00LXRgdGM0LrQsCDQvtCx0LvQsNGB0YLRjCwgNjUwMDA!5e0!3m2!1suk!2sua!4v1524221669656' width='100%' height='800' frameborder='0' style='border:0' allowfullscreen></iframe></div>"
            )
