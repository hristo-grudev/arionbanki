BOT_NAME = 'arionbanki'

SPIDER_MODULES = ['arionbanki.spiders']
NEWSPIDER_MODULE = 'arionbanki.spiders'
FEED_EXPORT_ENCODING = 'utf-8'
LOG_LEVEL = 'ERROR'
DOWNLOAD_DELAY = 0

ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
	'arionbanki.pipelines.ArionbankiPipeline': 100,

}