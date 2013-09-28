import re
import json
import requests
from lxml import etree

meta_tests = {
        'generator': {
            'Joomla'         : r'(?i)joomla!?\s*([\d\.]+)?',
            'vBulletin'      : r'vBulletin\s*(.*)',
            'WordPress'      : r'WordPress\s*(.*)',
            'XOOPS'          : r'xoops',
            'Plone'          : r'plone',
            'MediaWiki'      : r'(?i)MediaWiki',
            'CMSMadeSimple'  : r'(?i)CMS Made Simple',
            'SilverStripe'   : r'(?i)SilverStripe',
            'Movable Type'   : r'(?i)Movable Type',
            'Amiro.CMS'      : r'(?i)Amiro',
            'Koobi'          : r'(?i)koobi',
            'bbPress'        : r'(?i)bbPress',
            'DokuWiki'       : r'(?i)dokuWiki',
            'TYPO3'          : r'(?i)TYPO3',
            'PHP-Nuke'       : r'(?i)PHP-Nuke',
            'DotNetNuke'     : r'(?i)DotNetNuke',
            'Sitefinity'     : r'(?i)Sitefinity\s+(.*)',
            'WebGUI'         : r'(?i)WebGUI',
            'ez Publish'     : r'(?i)eZ\s*Publish',
            'BIGACE'         : r'(?i)BIGACE',
            'TypePad'        : r'(?i)typepad\.com',
            'Blogger'        : r'(?i)blogger',
            'PrestaShop'     : r'(?i)PrestaShop',
            'SharePoint'     : r'SharePoint',
            'JaliosJCMS'     : r'(?i)Jalios JCMS',
            'ZenCart'        : r'(?i)zen-cart',
            'WPML'           : r'(?i)WPML',
            'PivotX'         : r'(?i)PivotX',
            'OpenACS'        : r'(?i)OpenACS',
            'AlphaCMS'       : r'(?i)alphacms\s+(.*)',
            'concrete5'      : r'/concrete5 \s*(.*)$',
            'Webnode'        : r'Webnode',
            'GetSimple'      : r'GetSimple',
            'DataLifeEngine' : r'DataLife Engine',
            'ClanSphere'     : r'ClanSphere'
            },
        'copyright': {
            'phpBB': r'(?i)phpBB'
            },
        'elggrelease': {
            'Elgg': r'.+'
            },
        'powered-by': {
            'Serendipity': r'(?i)Serendipity',
            },
        'author': {
            'Avactis': r'(?i)Avactis Team',
            }
        }

script_tests = {
        'Google Analytics' : r'(?i)google-analytics.com(ga|urchin).js',
        'Quantcast'        : r'(?i)quantserve\.comquant\.js',
        'Prototype'        : r'(?i)prototype\.js',
        'Joomla'           : r'componentscom_',
        'Ubercart'         : r'(?i)uc_cart',
        'Closure'          : r'(?i)googbase\.js',
        'MODx'             : r'minb=.*f=.*',
        'MooTools'         : r'(?i)mootools',
        'Dojo'             : r'(?i)dojo(\.xd)?\.js',
        'script.aculo.us'  : r'(?i)scriptaculous\.js',
        'Disqus'           : r'(?i)disqus.comforums',
        'GetSatisfaction'  : r'(?i)getsatisfaction\.comfeedback',
        'Wibiya'           : r'(?i)wibiya\.comLoaders',
        'reCaptcha'        : r'(?i)(google\.comrecaptcha|api\.recaptcha\.net)',
        'Mollom'           : r'(?i)mollommollom\.js',
        'ZenPhoto'         : r'(?i)zp-corejs',
        'Gallery2'         : r'(?i)main\.php\?.*g2_.*',
        'AdSense'          : r'pageadshow_ads\.js',
        'XenForo'          : r'(?i)jsxenforo',
        'Cappuccino'       : r'FrameworksObjective-JObjective-J\.js',
        'Avactis'          : r'(?i)avactis-themes',
        'Volusion'         : r'ajjavascripts\.js',
        'AddThis'          : r'addthis\.comjs',
        'BuySellAds'       : r'buysellads.com.*bsa\.js',
        'Weebly'           : r'weebly\.comweebly',
        'Bootstrap'        : r'bootstrap-.*\.js',
        'Jigsy'            : r'javascriptsasterion\.js',
        'Yola'             : r'analytics\.yola\.net',
        'Alfresco'         : r'(alfresco)+(-min)?(scriptsmenu)?\.js',
        }

text_tests = {
        '1c-bitrix'        : r'(?i)<link[^>]*bitrix.*?>',
        'Closure'          : r'(?i)<script[^>]*>.*goog\.require',
        'Contao'           : r'(?i)powered by (TYPOlight|Contao)',
        'Fatwire'          : r'Satellite\?|ContentServer\?',
        'GoogleFontApi'    : r'(?i)ref=["\']?http://fonts.googleapis.com',
        'HumansTxt'        : r'(?i)<link[^>]*rel=[\'"]?author[\'"]?',
        'Liferay'          : r'(?i)<script[^>]*>.*LifeRay\.currentURL',
        'Magento'          : r'(?i)var BLANK_URL = \'[^>]+jsblank\.html\'',
        'miniBB'           : r'(?i)<a href=("|\')[^>]+minibb.+\s*<!--End of copyright link',
        'MODx'             : r'(?i)(<a[^>]+>Powered by MODx<a>|var el= \$\(\'modxhost\'\);|<script type=("|\')textjavascript("|\')>var MODX_MEDIA_PATH = "media";)',
        'Moodle'           : r'<link[^>]*themestandardstyles.php".*>|<link[^>]*themestyles.php\?theme=.*".*>',
        'OpenCart'         : r'index.php\?route=productproduct',
        'OpenCMS'          : r'(?i)<link[^>]*\.opencms\..*?>',
        'OpenX'            : r'(href|src)=["\'].*delivery(afr|ajs|avw|ck)\.php[^"\']*',
        'osCommerce'       : r'(product_info\.php\?products_id|_eof -->)',
        'PHP-Fusion'       : r'(?i)(href|src)=["\']?infusions',
        'Prostores'        : r'-legacycssAsset">',
        'Shibboleth'       : r'(?i)<form action="\'dpAuthnUserPassword" method="post">',
        'SMF'              : r'(?i)<script .+\s+var smf_',
        'Tumblr'           : r'(?i)<iframe src=("|\')http://\S+\.tumblr\.com',
        'vBulletin'        : r'(?i)vbmenu_control',
        'WordPress'        : r'(?i)<link rel=("|\')stylesheet("|\') [^>]+wp-content',
        #'GetSatisfaction' : r'(?i)asset_host\s*\+\s*"javascriptsfeedback.*\.js'gm,
        }


class Detector(object):
    def detect(self, url):
        print 'Running for', site_url
        try:
            self.r = requests.get(url)
            self.r.raise_for_status()
            self.document = etree.HTML(self.r.text)
            for name in dir(self):
                if name.startswith('do_'):
                    print 'running', name, '->',
                    type_ = getattr(self, name)()
                    if type_ is not None:
                        print type_
                        return type_
                    print None
        except (requests.RequestException, AttributeError):
            return None
        del self.document, self.r

    def do_meta(self):
        meta_items = self.document.xpath('//meta')
        for meta in meta_items:
            meta_name = meta.get('name')
            if meta_name not in meta_tests:
                continue
            for meta_test in meta_tests[meta_name].iteritems():
                type_, test = meta_test
                if re.match(test, meta.get('content')):
                    return type_

    def do_script(self):
        script_items = self.document.xpath('//script')
        for script in script_items:
            script_src = script.get('src')
            if not script_src:
                continue
            for type_, test in script_tests.iteritems():
                if re.match(test, script_src):
                    return type_

    def do_text(self):
        text = self.r.text
        for type_, test in text_tests.iteritems():
            #print test
            if re.match(test, text):
                return type_

if __name__ == '__main__':
    detector = Detector()
    for site in json.load(open('../data/sites/little.json'))['sites']:
        site_url = 'http://' + site
        type_ = detector.detect(site_url)
        print site_url, '->', type_
