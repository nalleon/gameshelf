package es.gameshelf.domain.services;

import es.gameshelf.domain.*;
import es.gameshelf.domain.interfaces.repository.IGameCollectionItemRepository;
import es.gameshelf.domain.interfaces.service.IGameCollectionItemService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

/**
 * @author Nabil L. A. @nalleon
 */
@Service
public class GameCollectionItemService implements IGameCollectionItemService {
    /**
     * Properties
     */
    IGameCollectionItemRepository repository;

    /**
     * Setter for the autowired service
     * @param repository of the service
     */
    @Autowired
    public void setRepository(IGameCollectionItemRepository repository) {
        this.repository = repository;
    }

    @Override
    public GameCollectionItem add(Game game, Collection collection, Format format, Platform platform, Edition edition, Region region) {
        GameCollectionItem item = new GameCollectionItem();
        item.setGame(game);
        item.setCollection(collection);
        item.setFormat(format);
        item.setPlatform(platform);
        item.setEdition(edition);
        item.setRegion(region);
        return repository.save(item);
    }

    @Override
    public List<GameCollectionItem> findAll() {
        return repository.findAll();
    }

    @Override
    public List<GameCollectionItem> findAllByRegion(Region region) {
        return repository.findAllByRegion(region);
    }

    @Override
    public List<GameCollectionItem> findAllByPlatform(Platform platform) {
        return repository.findAllByPlatform(platform);
    }

    @Override
    public List<GameCollectionItem> findAllByFormat(Format format) {
        return repository.findAllByFormat(format);
    }

    @Override
    public List<GameCollectionItem> findAllByEdition(Edition edition) {
        return repository.findAllByEdition(edition);
    }

    @Override
    public Map<Region, Integer> countAllGroupedByRegion() {
        return repository.countAllGroupedByRegion();
    }

    @Override
    public Map<Platform, Integer> countAllGroupedByPlatform() {
        return repository.countAllGroupedByPlatform();
    }

    @Override
    public Map<Format, Integer> countAllGroupedByFormat() {
        return repository.countAllGroupedByFormat();
    }

    @Override
    public Map<Edition, Integer> countAllGroupedByEdition() {
        return repository.countAllGroupedByEdition();
    }

    @Override
    public GameCollectionItem findById(Integer id) {
        return repository.findById(id);
    }

    @Override
    public List<GameCollectionItem> findAllByCollection(Collection collection) {
        return repository.findAllByCollection(collection);
    }

    @Override
    public List<GameCollectionItem> findAllInCollectionByAlphabeticalOrder(Collection collection) {
        return repository.findAllInCollectionByAlphabeticalOrder(collection);
    }

    @Override
    public List<GameCollectionItem> findAllInCollectionByOldestOrder(Collection collection) {
        return repository.findAllInCollectionByOldestOrder(collection);
    }

    @Override
    public List<GameCollectionItem> findAllInCollectionByLatestOrder(Collection collection) {
        return repository.findAllInCollectionByLatestOrder(collection);
    }

    @Override
    public Map<Region, Integer> countAllInCollectionGroupedByRegion(Collection collection) {
        return repository.countAllInCollectionGroupedByRegion(collection);
    }

    @Override
    public Map<Platform, Integer> countAllInCollectionGroupedByPlatform(Collection collection) {
        return repository.countAllInCollectionGroupedByPlatform(collection);
    }

    @Override
    public Map<Format, Integer> countAllInCollectionGroupedByFormat(Collection collection) {
        return repository.countAllInCollectionGroupedByFormat(collection);
    }

    @Override
    public Map<Edition, Integer> countAllInCollectionGroupedByEdition(Collection collection) {
        return repository.countAllInCollectionGroupedByEdition(collection);
    }

    @Override
    public List<GameCollectionItem> findAllInCollectionByRegion(Collection collection, Region region) {
        return repository.findAllInCollectionByRegion(collection, region);
    }

    @Override
    public List<GameCollectionItem> findAllInCollectionByPlatform(Collection collection, Platform platform) {
        return repository.findAllInCollectionByPlatform(collection, platform);
    }

    @Override
    public List<GameCollectionItem> findAllInCollectionByFormat(Collection collection, Format format) {
        return repository.findAllInCollectionByFormat(collection, format);
    }

    @Override
    public List<GameCollectionItem> findAllInCollectionByEdition(Collection collection, Edition edition) {
        return repository.findAllInCollectionByEdition(collection, edition);
    }

    @Override
    public List<GameCollectionItem> findAllInCollectionWithFilters(Collection collection, Region region, Platform platform, Format format, Edition edition) {
        return repository.findAllInCollectionWithFilters(collection, region,platform,format,edition);
    }

    @Override
    public boolean delete(Integer id) {
        return repository.delete(id);
    }

    @Override
    public GameCollectionItem update(Integer id, Game game, Collection collection, Format format, Platform platform, Edition edition, Region region) {
        GameCollectionItem item = new GameCollectionItem(id);
        item.setGame(game);
        item.setCollection(collection);
        item.setFormat(format);
        item.setPlatform(platform);
        item.setEdition(edition);
        item.setRegion(region);

        return repository.update(item);
    }
}
