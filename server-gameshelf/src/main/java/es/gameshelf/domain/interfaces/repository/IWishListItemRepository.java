package es.gameshelf.domain.interfaces.repository;

import es.gameshelf.domain.*;

import java.util.List;
import java.util.Map;

public interface IWishListItemRepository {
    WishListItem save(WishListItem wishListItem);
    List<WishListItem> findAll();
    List<WishListItem> findAllByRegion(Region region);
    List<WishListItem> findAllByPlatform(Platform platform);
    List<WishListItem> findAllByFormat(Format format);
    List<WishListItem> findAllByEdition(Edition edition);
    List<WishListItem> findAllByGame(Game game);
    
    Map<Region, Integer> countAllGroupedByRegion();
    Map<Platform, Integer> countAllGroupedByPlatform();
    Map<Format, Integer> countAllGroupedByFormat();
    Map<Edition, Integer> countAllGroupedByEdition();
    Map<Integer, Integer> countAllGroupedByPriority();
    int countAllGroupedByGame(Game game);
    int countAllGroupedByAnnotations();
    
    
    WishListItem findById(Integer id);
    
    List<WishListItem> findAllByUser(User user);
    List<WishListItem> findAllByUserInAlphabeticalOrder(User user);
    List<WishListItem> findAllByUserInOldestAdditionOrder(User user);
    List<WishListItem> findAllByUserInLatestAdditionOrder(User user);
    List<WishListItem> findAllByUserInHigherPriorityOrder(User user);
    List<WishListItem> findAllByUserInLowestPriorityOrder(User user);

    Map<Region, Integer> countAllByUserGroupedByRegion(User user);
    Map<Platform, Integer> countAllByUserGroupedByPlatform(User user);
    Map<Format, Integer> countAllByUserGroupedByFormat(User user);
    Map<Edition, Integer> countAllByUserGroupedByEdition(User user);
    Map<Integer, Integer> countAllByUserGroupedByPriority(User user);

    List<WishListItem> findAllByUserAndRegion(User user, Region region);
    List<WishListItem> findAllByUserAndPlatform(User user, Platform platform);
    List<WishListItem> findAllByUserAndFormat(User user, Format format);
    List<WishListItem> findAllByUserAndEdition(User user, Edition edition);
    List<WishListItem> findAllByUserAndPriority(User user, Integer priority);

    List<WishListItem> findAllByUserWithFilters(User user, Region region, Platform platform,
                                                            Format format, Edition edition, Integer priority);
    boolean delete(Integer id);
    WishListItem update(WishListItem wishListItem);
}
