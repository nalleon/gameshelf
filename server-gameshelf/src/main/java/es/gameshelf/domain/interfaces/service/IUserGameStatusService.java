package es.gameshelf.domain.interfaces.service;

import es.gameshelf.domain.Game;
import es.gameshelf.domain.Status;
import es.gameshelf.domain.User;
import es.gameshelf.domain.UserGameStatusItem;

import java.util.List;
import java.util.Map;

/**
 * @author Nabil L. A. @nalleon
 */
public interface IUserGameStatusService {
    UserGameStatusItem add(float userRating, String annotation, User user, Game game, Status status);

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
    UserGameStatusItem update(Integer id, float userRating, String annotation, User user, Game game, Status status);
    UserGameStatusItem updateRating(Integer id, float userRating);
    UserGameStatusItem updateAnnotation(Integer id, String annotation);
    UserGameStatusItem updateStatus(Integer id, Status status);
}
