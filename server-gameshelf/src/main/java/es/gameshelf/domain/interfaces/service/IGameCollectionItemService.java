package es.gameshelf.domain.interfaces.service;

import es.gameshelf.domain.*;

import java.util.List;
import java.util.Map;

/**
 * @author Nabil L. A. @nalleon
 */
public interface IGameCollectionItemService {
    GameCollectionItem add(Game game, Collection collection, Format format, Platform platform, Edition edition, Region region);
    List<GameCollectionItem> findAll();
    List<GameCollectionItem> findAllByRegion(Region region);
    List<GameCollectionItem> findAllByPlatform(Platform platform);
    List<GameCollectionItem> findAllByFormat(Format format);
    List<GameCollectionItem> findAllByEdition(Edition edition);
    Map<Region, Integer> countAllGroupedByRegion();
    Map<Platform, Integer> countAllGroupedByPlatform();
    Map<Format, Integer> countAllGroupedByFormat();
    Map<Edition, Integer> countAllGroupedByEdition();
    GameCollectionItem findById(Integer id);
    List<GameCollectionItem> findAllByCollection(Collection collection);
    List<GameCollectionItem> findAllInCollectionByAlphabeticalOrder(Collection collection);
    List<GameCollectionItem> findAllInCollectionByOldestOrder(Collection collection);
    List<GameCollectionItem> findAllInCollectionByLatestOrder(Collection collection);
    Map<Region, Integer> countAllInCollectionGroupedByRegion(Collection collection);
    Map<Platform, Integer> countAllInCollectionGroupedByPlatform(Collection collection);
    Map<Format, Integer> countAllInCollectionGroupedByFormat(Collection collection);
    Map<Edition, Integer> countAllInCollectionGroupedByEdition(Collection collection);
    List<GameCollectionItem> findAllInCollectionByRegion(Collection collection, Region region);
    List<GameCollectionItem> findAllInCollectionByPlatform(Collection collection, Platform platform);
    List<GameCollectionItem> findAllInCollectionByFormat(Collection collection, Format format);
    List<GameCollectionItem> findAllInCollectionByEdition(Collection collection, Edition edition);
    List<GameCollectionItem> findAllInCollectionWithFilters(Collection collection, Region region, Platform platform, Format format, Edition edition);
    boolean delete(Integer id);
    GameCollectionItem update(Integer id, Game game, Collection collection, Format format, Platform platform, Edition edition, Region region);
}
