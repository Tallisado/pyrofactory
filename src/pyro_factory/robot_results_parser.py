from datetime import datetime
from hashlib import sha1
from robot.api import ExecutionResult
from logger import Logger

class RobotResults(object):
    def __init__(self, suite_name,
                       imported_at,
                       source,
                       start_time,
                       end_time,
                       #err_level, err_timestamp, err_message,
                       test#test_name,elapsed,passed,failed
        ):
        print test
        self._suite_name = suite_name
        self._test_name = test['name']
        self._elapsed = test['elapsed']
        self._passed = test['passed']
        self._failed = test['failed']
        
    @property
    def suite(self):
        return self._suite_name
    
    @property
    def testname(self):
        return self._test_name
    
    @property
    def elapsed(self):
        return self._elapsed
    
    @property
    def passed(self):
        return self._passed    
    
    @property
    def failed(self):
        return self._failed
        
class RobotResultsParser(object):

    def __init__(self, include_keywords, verbose_stream):
        self._verbose = Logger('Parser', verbose_stream)
        self._include_keywords = include_keywords

    def xml_to_object(self, xml_file, suite_name):
        self._verbose('- Parsing %s' % xml_file)
        test_run = ExecutionResult(xml_file, include_keywords=self._include_keywords)
        #hash = self._hash(xml_file)

        return RobotResults(
            suite_name,
            datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f'),
            test_run.source,
            self._format_robot_timestamp(test_run.suite.starttime),
            self._format_robot_timestamp(test_run.suite.endtime),
            #self._parse_errors(test_run.errors.messages),
            self._parse_statistics(test_run.statistics),
            #self._parse_suite(test_run.suite)
        )               

    # def _hash(self, xml_file):
        # block_size = 68157440
        # hasher = sha1()
        # with open(xml_file, 'rb') as f:
            # chunk = f.read(block_size)
            # while len(chunk) > 0:
                # hasher.update(chunk)
                # chunk = f.read(block_size)
        # return hasher.hexdigest()

    # def _parse_errors(self, errors):
        # [(error.level, self._format_robot_timestamp(error.timestamp), error.message)
            # for error in errors]

    def _parse_statistics(self, statistics):
        return self._parse_test_run_statistics(statistics.total)
        # self._parse_tag_statistics(statistics.tags, test_run_id)

    def _parse_test_run_statistics(self, test_run_statistics):
        # self._verbose('`--> Parsing test run statistics')
        return [self._parse_test_run_stats(stat) for stat in test_run_statistics][0]

    # def _parse_tag_statistics(self, tag_statistics, test_run_id):
        # self._verbose('  `--> Parsing tag statistics')
        # [self._parse_tag_stats(stat, test_run_id) for stat in tag_statistics.tags.values()]

    # def _parse_tag_stats(self, stat, test_run_id):
        # self._db.insert_or_ignore('tag_status', {
            # 'test_run_id': test_run_id,
            # 'name': stat.name,
            # 'critical': stat.critical,
            # 'elapsed': getattr(stat, 'elapsed', None),
            # 'failed': stat.failed,
            # 'passed': stat.passed
        # })

    def _parse_test_run_stats(self, stat):
        #{'name'stat.name,getattr(stat, 'elapsed', None),stat.failed,stat.passed)]
        if stat.name == 'Critical Tests':
            return {'name':stat.name, 'elapsed':getattr(stat, 'elapsed', None), 'failed':stat.failed, 'passed':stat.passed}

    # def _parse_suite(self, suite, test_run_id, parent_suite_id=None):
        # self._verbose('`--> Parsing suite: %s' % suite.name)
        # try:
            # suite_id = self._db.insert('suites', {
                # 'suite_id': parent_suite_id,
                # 'xml_id': suite.id,
                # 'name': suite.name,
                # 'source': suite.source,
                # 'doc': suite.doc
            # })
        # except IntegrityError:
            # suite_id = self._db.fetch_id('suites', {
                # 'name': suite.name,
                # 'source': suite.source
            # })
        # self._parse_suite_status(test_run_id, suite_id, suite)
        # self._parse_suites(suite, test_run_id, suite_id)
        # self._parse_tests(suite.tests, test_run_id, suite_id)
        # self._parse_keywords(suite.keywords, test_run_id, suite_id, None)

    # def _parse_suite_status(self, test_run_id, suite_id, suite):
        # self._db.insert_or_ignore('suite_status', {
            # 'test_run_id': test_run_id,
            # 'suite_id': suite_id,
            # 'passed': suite.statistics.all.passed,
            # 'failed': suite.statistics.all.failed,
            # 'elapsed': suite.elapsedtime,
            # 'status': suite.status
        # })

    # def _parse_suites(self, suite, test_run_id, parent_suite_id):
        # [self._parse_suite(subsuite, test_run_id, parent_suite_id) for subsuite in suite.suites]

    # def _parse_tests(self, tests, test_run_id, suite_id):
        # [self._parse_test(test, test_run_id, suite_id) for test in tests]

    # def _parse_test(self, test, test_run_id, suite_id):
        # self._verbose('  `--> Parsing test: %s' % test.name)
        # try:
            # test_id = self._db.insert('tests', {
                # 'suite_id': suite_id,
                # 'xml_id': test.id,
                # 'name': test.name,
                # 'timeout': test.timeout,
                # 'doc': test.doc
            # })
        # except IntegrityError:
            # test_id = self._db.fetch_id('tests', {
                # 'suite_id': suite_id,
                # 'name': test.name
            # })
        # self._parse_test_status(test_run_id, test_id, test)
        # self._parse_tags(test.tags, test_id)
        # self._parse_keywords(test.keywords, test_run_id, None, test_id)

    # def _parse_test_status(self, test_run_id, test_id, test):
        # self._db.insert_or_ignore('test_status', {
            # 'test_run_id': test_run_id,
            # 'test_id': test_id,
            # 'status': test.status,
            # 'elapsed': test.elapsedtime
        # })

    # def _parse_tags(self, tags, test_id):
        # self._db.insert_many_or_ignore('tags', ('test_id', 'content'),
            # [(test_id, tag) for tag in tags]
        # )

    # def _parse_keywords(self, keywords, test_run_id, suite_id, test_id, keyword_id=None):
        # if self._include_keywords:
            # [self._parse_keyword(keyword, test_run_id, suite_id, test_id, keyword_id)
            # for keyword in keywords]

    # def _parse_keyword(self, keyword, test_run_id, suite_id, test_id, keyword_id):
        # try:
            # keyword_id = self._db.insert('keywords', {
                # 'suite_id': suite_id,
                # 'test_id': test_id,
                # 'keyword_id': keyword_id,
                # 'name': keyword.name,
                # 'type': keyword.type,
                # 'timeout': keyword.timeout,
                # 'doc': keyword.doc
            # })
        # except IntegrityError:
            # keyword_id = self._db.fetch_id('keywords', {
                # 'name': keyword.name,
                # 'type': keyword.type
            # })
        # self._parse_keyword_status(test_run_id, keyword_id, keyword)
        # self._parse_messages(keyword.messages, keyword_id)
        # self._parse_arguments(keyword.args, keyword_id)
        # self._parse_keywords(keyword.keywords, test_run_id, None, None, keyword_id)

    # def _parse_keyword_status(self, test_run_id, keyword_id, keyword):
        # self._db.insert_or_ignore('keyword_status', {
            # 'test_run_id': test_run_id,
            # 'keyword_id': keyword_id,
            # 'status': keyword.status,
            # 'elapsed': keyword.elapsedtime
        # })

    # def _parse_messages(self, messages, keyword_id):
        # self._db.insert_many_or_ignore('messages', ('keyword_id', 'level', 'timestamp', 'content'),
            # [(keyword_id, message.level, self._format_robot_timestamp(message.timestamp),
            # message.message) for message in messages]
        # )

    # def _parse_arguments(self, args, keyword_id):
        # self._db.insert_many_or_ignore('arguments', ('keyword_id', 'content'),
            # [(keyword_id, arg) for arg in args]
        # )

    def _format_robot_timestamp(self, timestamp):
        return datetime.strptime(timestamp, '%Y%m%d %H:%M:%S.%f')