#!/usr/bin/env python
# coding=utf-8


import json
import copy
import logging
from enum import Enum
from pathlib import PurePath, Path

from tree_struct_config import (
    IntLeaf,
    StringLeaf,
    BooleanLeaf,
    ListLeaf,

    Branch,

    Root,
    SerializationFormat,
    SerializationDecodeError,
)

DEFAULT_CONFIG_FILE = 'dnsdam.toml'
DEFAULT_CONFIG_FILE_PATH_LIST = [
    '.',
    '/etc'
]

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 53

RESOLVER_DEFAULT_UPSTREAM_IP_ADDRESS_V4 = '114.114.114.114'
RESOLVER_DEFAULT_TIMEOUT = 15  # windows default dns request timeout is 15 seconds

# MemoryCache: 'memory:///'
# RedisCache:  'redis://:password@localhost:port/0'
CACHE_DEFAULT_URI = 'memory:///'
CACHE_DEFAULT_LIFETIME = 60 * 15  # 15 minute
CACHE_DEFAULT_STORAGE_LIFETIME = 60 * 60 * 24 * 100  # 100 day

logger = logging.getLogger(__file__)


class DNSResolverType(Enum):
    UDP = 1
    TCP = 2
    DoT = 3
    DoH = 4


class ConfigException(Exception):
    pass


class UpstreamResolver(Root):
    # name = StringLeaf('default')
    # type = DNSResolverType.UDP.name
    # ip_address = StringLeaf(RESOLVER_DEFAULT_UPSTREAM_IP_ADDRESS_V4)
    # ip_address6 = StringLeaf()
    #
    # timeout = IntLeaf(RESOLVER_DEFAULT_TIMEOUT)
    # proxy = StringLeaf()
    #
    # lifetime = IntLeaf(CACHE_DEFAULT_LIFETIME)  # 60 * 15 = 15 minute

    def __init__(self):
        self.name = StringLeaf('default')
        self.type = DNSResolverType.UDP.name
        self.ip_address = StringLeaf(RESOLVER_DEFAULT_UPSTREAM_IP_ADDRESS_V4)
        self.ip_address6 = StringLeaf()

        self.timeout = IntLeaf(RESOLVER_DEFAULT_TIMEOUT)
        self.proxy = StringLeaf()

        self.lifetime = IntLeaf(CACHE_DEFAULT_LIFETIME)  # 60 * 15 = 15 minute

        super().__init__()

    def loads(self, s, serialization_format=None):
        # super().loads(copy.deepcopy(s), serialization_format)
        super().loads(s, serialization_format)

        try:
            self.type = DNSResolverType.__getitem__(self.type)
        except KeyError:
            self.type = DNSResolverType.UDP

        if self.ip_address == '':
            self.ip_address = None
        if self.ip_address6 == '':
            self.ip_address6 = None

        return

    def __str__(self):
        return '{}|{}|{}|{}|{}|{}'.format(  # TODO: update tree_struct_config
            self.name, self.type, self.ip_address, self.ip_address6, self.timeout, self.proxy, self.lifetime
        )


class Config(Root):
    class Common(Branch):
        sentry_dsn = StringLeaf()

    class Service(Branch):
        bind = StringLeaf(DEFAULT_HOST)
        port = IntLeaf(DEFAULT_PORT)

    class Cache(Branch):
        uri = StringLeaf(CACHE_DEFAULT_URI)
        storage_lifetime = IntLeaf(CACHE_DEFAULT_STORAGE_LIFETIME)

    class FakeDNS(Branch):
        a_record = ListLeaf()

    class Default(Branch):
        resolver = StringLeaf('default')

    UpstreamResolver = ListLeaf()
    upstream_resolvers = dict()

    Group = ListLeaf()
    groups = dict()

    # override dump/load function
    load_succeed = False

    def load(self, fp=None, filename=DEFAULT_CONFIG_FILE, serialization_format=SerializationFormat.TOML):
        if filename:
            full_filename_list = [filename, ]

        else:
            full_filename_list = []
            for path in DEFAULT_CONFIG_FILE_PATH_LIST:
                full_filename_list.append(PurePath(path).joinpath(DEFAULT_CONFIG_FILE).as_posix())

        load_succeed = False
        for full_filename in full_filename_list:
            if not Path(full_filename).exists():
                continue

            with open(full_filename) as fp:
                try:
                    super().load(fp, serialization_format)
                    load_succeed = True
                    logger.info('DNS Dam load config from: {}'.format(full_filename))
                    break

                except SerializationDecodeError as e:
                    raise ConfigException('load config file failed! {}'.format(e))

        if not load_succeed:
            raise ConfigException('load config file failed!')

        for upstream in self.UpstreamResolver:
            # print('1111', upstream)
            # upstream_resolver = copy.deepcopy(UpstreamResolver())
            upstream_resolver = UpstreamResolver()
            # print('2222', upstream_resolver)
            upstream_resolver.loads(json.dumps(upstream))
            # print(111, upstream_resolver)

            # self.upstream_resolvers[upstream_resolver.name] = upstream_resolver
            name = copy.deepcopy(upstream_resolver.name)
            self.upstream_resolvers[name] = copy.deepcopy(upstream_resolver)
            # sss = copy.deepcopy(upstream_resolver)
            # self.upstream_resolvers[sss.name] = copy.deepcopy(sss)
            # logger.debug('loaded: {}, {}'.format(
            #     upstream_resolver.name, self.upstream_resolvers[upstream_resolver.name]
            # ))
            # logger.debug('loaded: {}'.format(upstream_resolver))

        for key in self.upstream_resolvers:
            print(type(self.upstream_resolvers[key]), self.upstream_resolvers[key])
        # for key in self.groups:
        #     print(self.groups[key], self.groups[key].name)

        return


def main():
    try:
        config = Config()
        config.load(filename='demo2.toml')
    except ConfigException as e:
        logger.error(e)
        return


if __name__ == '__main__':
    main()
