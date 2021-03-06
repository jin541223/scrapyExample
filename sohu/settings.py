# -*- coding: utf-8 -*-

# Scrapy settings for sohu project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'sohu'

SPIDER_MODULES = ['sohu.spiders']
NEWSPIDER_MODULE = 'sohu.spiders'
DOWNLOAD_HANDLERS = {'s3': None, }


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'sohu (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY=30
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
#COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept':'*/*',
#   'Accept-Encoding':'gzip, deflate, sdch',
#   'Accept-Language':'zh-CN,zh;q=0.8',
#   'Cache-Control':'max-age=0',
#   'Connection':'keep-alive',
#   'Cookie':'vjuids=2112f5119.15509f95379.0.98d5f2dcfdba1; IPLOC=CN4403; SUV=1606011119423036; networkmp_del=check:1; sohutag=8HsmeSc5NCwmcyc5NCwmYjc5NCwmYSc5NCwmZjc5NCwmZyc5NCwmbjc5NCwmaSc5NCwmdyc5NSwmaCc5NCwmYyc5NCwmZSc5NCwmbSc5NCwmdCc5NH0; _ga=GA1.2.1585468001.1464920034; JSESSIONID=aaaZX3tFHnPxA8L0yLvuv; beans_12512=visit:2; beans_13626=visit:2; viewCarW=2015%u6B3E%20TT%20Coupe%2045%20TFSI%2C130015%2Cjinkouaudi%2C1552%7C2015%u6B3E%20TT%20Coupe%2045%20TFSI%20quattro%2C130016%2Cjinkouaudi%2C1552%7C2016%u6B3E%203.0T%20%u8C6A%u534E%u578B%2C130586%2Caudis%2C1570%7C2014%u6B3E%201.5L%20%u81EA%u52A8%u5C0A%u5C1A%u578B%2C126844%2Cdongfengfengshen-2066%2C4509%7C2016%u6B3E%201.5L%20%u624B%u52A8%u5B9E%u5C1A%u578B%2C133177%2Cdongfengfengshen-2066%2C4509%7C2015%u6B3E%201.4T%20%u624B%u52A8%u98CE%u5C1A%u72485%u5EA7%2C126603%2Cshanghaivw%2C1086%7C2016%u6B3E%20TFSI%20%u8212%u9002%u578B%2C131888%2Cyiqiaudi%2C2051%7C2010%u6B3E%206.0L%2C114640%2Castonmartin-1107%2C2575%7C2013%u6B3E%206.0L%20S%2C123512%2Castonmartin-1107%2C2575%7C2014%u6B3E%206.0L%20S%20%u767E%u5E74%u7EAA%u5FF5%u7248%2C124351%2Castonmartin-1107%2C2575%7C2015%u6B3E%206.0L%20S%2C130069%2Castonmartin-1107%2C2575%7C2015%u6B3E%20335i%20xDrive%2C126957%2Cjinkoubmw%2C3087%7C2016%u6B3E%2030%20TFSI%20%u6807%u51C6%u578B%2C132990%2Cyiqiaudi%2C3909%7C2016%u6B3E%205.2T%20%u57FA%u672C%u578B%2C133004%2Castonmartin-1107%2C4986%7C2016%u6B3E%201.6L%20%u81EA%u52A8%u5341%u5468%u5E74%u7EAA%u5FF5%u7248%2C132467%2Cbesturn-2047%2C4786%7C2016%u6B3E%20M2%2C132971%2Cbmwm%2C4288%7C2012%u6B3E%2035%20GC%2C123135%2Cbrabus-2098%2C3610%7C2016%u6B3E%2040%20TFSI%20%u8FDB%u53D6%u578B%2C130957%2Cyiqiaudi%2C1571%7C2016%u6B3E%2040%20TFSI%20%u8C6A%u534E%u578B%2C130961%2Cyiqiaudi%2C1571%7C2015%u6B3E%20E180L%20%u8FD0%u52A8%u578B%2C127877%2Cbeijingbenz%2C2976%7C2016%u6B3E%20CLA%20200%20%u52A8%u611F%u578B%2C131727%2Cjinkoubenz%2C3537%7C2014%u6B3E%2030%20TFSI%20%u6280%u672F%u578B%2C123937%2Cjinkouaudi%2C1572; vjlast=1464751183.1465174894.11; ipcncode=CN440300',
#   'Host':'db.auto.sohu.com',
#   'Referer':'http://db.auto.sohu.com/jinkouaudi/1552/130016/maintenance.html',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'sohu.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'sohu.middlewares.Middleware.SetHeaderMiddleware': 543,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'sohu.pipelines.SomePipeline': 300,
#}

ITEM_PIPELINES = {
    'sohu.pipelines.pipeline': 300,
}

# 数据库连接配置
DB_CONN='mysql+pymysql://webserver:webserver@localhost/DB_NAME?charset=utf8'

# 数据库调试
DB_DEBUG=False

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
# AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'
