package es.gameshelf.domain.services;

import es.gameshelf.domain.*;
import es.gameshelf.domain.interfaces.repository.IWishListItemRepository;
import es.gameshelf.domain.interfaces.service.IWishListItemService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.List;
import java.util.Map;

/**
 * @author Nabil L. A. @nalleon
 */
@Service
public class WishListItemService implements IWishListItemService {

    /**
     * Properties
     */
    IWishListItemRepository repository;

    /**
     * Setter for the autowired service
     * @param repository of the service
     */
    @Autowired
    public void setRepository(IWishListItemRepository repository) {
        this.repository = repository;
    }

    @Override
    public WishListItem add(int priority, String annotation, Format format, Platform platform, Edition edition, Region region, Game game, User user) {
        WishListItem item = new WishListItem();
        item.setPriority(priority);
        item.setAnnotation(annotation);
        item.setFormat(format);
        item.setPlatform(platform);
        item.setEdition(edition);
        item.setRegion(region);
        item.setGame(game);
        item.setUser(user);

        return repository.save(item);
    }

    @Override
    public List<WishListItem> findAll() {
        return repository.findAll();
    }

    @Override
    public List<WishListItem> findAllByRegion(Region region) {
        return repository.findAllByRegion(region);
    }

    @Override
    public List<WishListItem> findAllByPlatform(Platform platform) {
        return repository.findAllByPlatform(platform);
    }

    @Override
    public List<WishListItem> findAllByFormat(Format format) {
        return repository.findAllByFormat(format);
    }

    @Override
    public List<WishListItem> findAllByEdition(Edition edition) {
        return repository.findAllByEdition(edition);
    }

    @Override
    public List<WishListItem> findAllByGame(Game game) {
        return repository.findAllByGame(game);
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
    public Map<Integer, Integer> countAllGroupedByPriority() {
        return repository.countAllGroupedByPriority();
    }

    @Override
    public int countAllGroupedByGame(Game game) {
        return repository.countAllGroupedByGame(game);
    }

    @Override
    public int countAllGroupedByAnnotations() {
        return repository.countAllGroupedByAnnotations();
    }

    @Override
    public WishListItem findById(Integer id) {
        return repository.findById(id);
    }

    @Override
    public List<WishListItem> findAllByUser(User user) {
        return repository.findAllByUser(user);
    }

    @Override
    public List<WishListItem> findAllByUserInAlphabeticalOrder(User user) {
        return repository.findAllByUserInAlphabeticalOrder(user);
    }

    @Override
    public List<WishListItem> findAllByUserInOldestAdditionOrder(User user) {
        return repository.findAllByUserInOldestAdditionOrder(user);
    }

    @Override
    public List<WishListItem> findAllByUserInLatestAdditionOrder(User user) {
        return repository.findAllByUserInLatestAdditionOrder(user);
    }

    @Override
    public List<WishListItem> findAllByUserInHigherPriorityOrder(User user) {
        return repository.findAllByUserInHigherPriorityOrder(user);
    }

    @Override
    public List<WishListItem> findAllByUserInLowestPriorityOrder(User user) {
        return repository.findAllByUserInLowestPriorityOrder(user);
    }

    @Override
    public Map<Region, Integer> countAllByUserGroupedByRegion(User user) {
        return repository.countAllByUserGroupedByRegion(user);
    }

    @Override
    public Map<Platform, Integer> countAllByUserGroupedByPlatform(User user) {
        return repository.countAllByUserGroupedByPlatform(user);
    }

    @Override
    public Map<Format, Integer> countAllByUserGroupedByFormat(User user) {
        return repository.countAllByUserGroupedByFormat(user);
    }

    @Override
    public Map<Edition, Integer> countAllByUserGroupedByEdition(User user) {
        return repository.countAllByUserGroupedByEdition(user);
    }

    @Override
    public Map<Integer, Integer> countAllByUserGroupedByPriority(User user) {
        return repository.countAllByUserGroupedByPriority(user);
    }

    @Override
    public List<WishListItem> findAllByUserAndRegion(User user, Region region) {
        return repository.findAllByUserAndRegion(user,region);
    }

    @Override
    public List<WishListItem> findAllByUserAndPlatform(User user, Platform platform) {
        return repository.findAllByUserAndPlatform(user,platform);
    }

    @Override
    public List<WishListItem> findAllByUserAndFormat(User user, Format format) {
        return repository.findAllByUserAndFormat(user, format);
    }

    @Override
    public List<WishListItem> findAllByUserAndEdition(User user, Edition edition) {
        return repository.findAllByUserAndEdition(user,edition);
    }

    @Override
    public List<WishListItem> findAllByUserAndPriority(User user, Integer priority) {
        return repository.findAllByUserAndPriority(user, priority);
    }

    @Override
    public List<WishListItem> findAllByUserWithFilters(User user, Region region, Platform platform, Format format,
                                                       Edition edition, Integer priority) {
        return repository.findAllByUserWithFilters(user,region,platform,format,edition,priority);
    }

    @Override
    public boolean delete(Integer id) {
        return repository.delete(id);
    }

    @Override
    public WishListItem update(Integer id, int priority, String annotation, Format format, Platform platform,
                               Edition edition, Region region, Game game, User user) {
        WishListItem item = new WishListItem();
        item.setId(id);
        item.setPriority(priority);
        item.setAnnotation(annotation);
        item.setFormat(format);
        item.setPlatform(platform);
        item.setEdition(edition);
        item.setRegion(region);
        item.setGame(game);
        item.setUser(user);

        return repository.update(item);
    }

    @Override
    public WishListItem updatePriority(Integer id, int priority) {
        WishListItem item = new WishListItem();
        item.setId(id);
        item.setPriority(priority);

        return repository.update(item);
    }

    @Override
    public WishListItem updateAnnotation(Integer id, String annotation) {
        WishListItem item = new WishListItem();
        item.setId(id);
        item.setAnnotation(annotation);

        return repository.update(item);
    }
}
