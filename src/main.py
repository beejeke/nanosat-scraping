from methods import SatelliteScraper

if __name__ == '__main__':

    scraper = SatelliteScraper()
    scraper.scraper()
    scraper.save_data_csv()