package es.gameshelf.domain.interfaces.repository;

import es.gameshelf.domain.*;

import java.util.List;
import java.util.Map;
/**
 * @author Nabil L. A. @nalleon
 */
public interface IUserGameStatusRepository {
    UserGameStatusItem save(UserGameStatusItem uGStatus);

    List<UserGameStatusItem> findAll();
    List<UserGameStatusItem> findAllByGame(Game game);
    List<UserGameStatusItem> findAllByStatus(Status status);
    List<UserGameStatusItem> findAllByUserAlphabeticalOrder(User user);
    List<UserGameStatusItem> findAllByUserOldestOrder(User user);
    List<UserGameStatusItem> findAllByUserLatestOrder(User user);
    UserGameStatusItem findById(Integer id);

    Map<Status, Integer> countAllGroupedByStatus();;
    int countAllGroupedByGame(Game game);
    int countAllGroupedByGameAndStatus(Game game, Status status);

    List<UserGameStatusItem> findAllByUser(User user);
    List<UserGameStatusItem> findAllByUserAndStatus(User user, Status status);

    Map<Status, Integer> countAllByUserGroupedByStatus(User user);
    int countAllByUserGroupedBySpecificStatus(User user, Status status);

    boolean delete(Integer id);
    UserGameStatusItem update(UserGameStatusItem uGStatus);
    UserGameStatusItem updateRating(UserGameStatusItem uGStatus);
    UserGameStatusItem updateAnnotation(UserGameStatusItem uGStatus);
    UserGameStatusItem updateStatus(UserGameStatusItem uGStatus);

}
