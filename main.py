import csv
import datetime
import logging
import multiprocessing
import time

import dns.resolver
import tqdm

cpu_count = multiprocessing.cpu_count()
logging.basicConfig(filename=f'domains.log', level=logging.WARNING,
                    format="%(asctime)s %(name)-30s %(levelname)-8s %(message)s")
myResolver = dns.resolver.Resolver()

# Change these in whatever you like.
# Default is using Cloudflare, Google and OpenDNS
myResolver.nameservers = ['1.1.1.1', '1.0.0.1', '8.8.8.8', '8.8.4.4', '208.67.222.222', '208.67.220.220']


def check_domain_existence(domain):
    """Given a domain name, tries to resolve its NS and A records using the nameservers given above. Returns a dict for
    easy saving as JSON, format {'domain': domain_name:str, 'exists': True/False:bool}"""
    logging.info(f'Checking {domain}')
    t0 = time.time()
    try:
        myResolver.resolve(qname=domain, rdtype='NS', lifetime=2)
        t1 = time.time()
        logging.info(f'Checking {domain} took {(t1 - t0) * 1000}ms')
        return {'domain': domain,'exists': True}
    except:
        try:
            myResolver.resolve(qname=domain, rdtype='A', lifetime=2)
            t1 = time.time()
            logging.info(f'Checking {domain} took {(t1 - t0) * 1000}ms')
            return {'domain': domain, 'exists': True}
        except (dns.resolver.NXDOMAIN, dns.resolver.NoNameservers, dns.exception.Timeout, dns.resolver.NoAnswer):
            t1 = time.time()
            logging.info(f'Checking {domain} took {(t1 - t0) * 1000}ms')
            return {'domain': domain, 'exists': False}


def get_tlds() -> list:
    """Extracts third level domain from a file called "tlds.txt" in the working dir. Tlds must be separated by newline"""
    with open('tlds.txt', 'r') as tld_file:
        data = tld_file.read().split('\n')
    return data


def make_domain_names(name):
    """Given a name, uses it to make a list of strings representing all possible domain names with that name as 2ld"""
    tlds = get_tlds()
    domain_names = [f"{name}.{tld.lower()}" for tld in tlds]
    return domain_names


if __name__ == '__main__':
    print('Type a domain name you want to check, with no TLD')
    now = datetime.datetime.now().strftime("%H_%M")
    name = input('>>>')
    domains = make_domain_names(name)
    result = []
    with multiprocessing.Pool(processes=cpu_count) as pool, tqdm.tqdm(total=len(domains)) as pbar:
        for data in pool.imap_unordered(check_domain_existence, domains):
            result.append(data)
            pbar.update()
    chiavi = list(set([i for s in [d.keys() for d in result] for i in s]))
    with open(f'result{name}_{now}.csv', 'w+', newline='', encoding="utf8") as csvfile:
        wr = csv.DictWriter(csvfile, quoting=csv.QUOTE_ALL, fieldnames=chiavi, restval="",)
        wr.writeheader()
        wr.writerows(result)
    print("Done! You will find a CSV file with your results in the working directory")
