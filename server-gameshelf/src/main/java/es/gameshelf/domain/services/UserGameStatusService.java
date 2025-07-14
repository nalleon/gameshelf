package es.gameshelf.domain.services;

import es.gameshelf.domain.Game;
import es.gameshelf.domain.Status;
import es.gameshelf.domain.User;
import es.gameshelf.domain.UserGameStatusItem;
import es.gameshelf.domain.interfaces.repository.IUserGameStatusRepository;
import es.gameshelf.domain.interfaces.service.IUserGameStatusService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

/**
 * @author Nabil L. A. @nalleon
 */
@Service
public class UserGameStatusService implements IUserGameStatusService {

    /**
     * Properties
     */
    IUserGameStatusRepository repository;

    /**
     * Setter for the autowired service
     * @param repository of the service
     */
    @Autowired
    public void setRepository(IUserGameStatusRepository repository) {
        this.repository = repository;
    }

    @Override
    public UserGameStatusItem add(float userRating, String annotation, User user, Game game, Status status) {
        UserGameStatusItem item = new UserGameStatusItem();
        item.setUserRating(userRating);
        item.setAnnotation(annotation);
        item.setUser(user);
        item.setGame(game);
        item.setStatus(status);

        return repository.save(item);
    }

    @Override
    public List<UserGameStatusItem> findAll() {
        return repository.findAll();
    }

    @Override
    public List<UserGameStatusItem> findAllByGame(Game game) {
        return repository.findAllByGame(game);
    }

    @Override
    public List<UserGameStatusItem> findAllByStatus(Status status) {
        return repository.findAllByStatus(status);
    }

    @Override
    public List<UserGameStatusItem> findAllByUserAlphabeticalOrder(User user) {
        return repository.findAllByUserAlphabeticalOrder(user);
    }

    @Override
    public List<UserGameStatusItem> findAllByUserOldestOrder(User user) {
        return repository.findAllByUserOldestOrder(user);
    }

    @Override
    public List<UserGameStatusItem> findAllByUserLatestOrder(User user) {
        return repository.findAllByUserLatestOrder(user);
    }

    @Override
    public UserGameStatusItem findById(Integer id) {
        return repository.findById(id);
    }

    @Override
    public Map<Status, Integer> countAllGroupedByStatus() {
        return repository.countAllGroupedByStatus();
    }

    @Override
    public int countAllGroupedByGame(Game game) {
        return repository.countAllGroupedByGame(game);
    }

    @Override
    public int countAllGroupedByGameAndStatus(Game game, Status status) {
        return repository.countAllGroupedByGameAndStatus(game,status);
    }

    @Override
    public List<UserGameStatusItem> findAllByUser(User user) {
        return repository.findAllByUser(user);
    }

    @Override
    public List<UserGameStatusItem> findAllByUserAndStatus(User user, Status status) {
        return repository.findAllByUserAndStatus(user,status);
    }

    @Override
    public Map<Status, Integer> countAllByUserGroupedByStatus(User user) {
        return repository.countAllByUserGroupedByStatus(user);
    }

    @Override
    public int countAllByUserGroupedBySpecificStatus(User user, Status status) {
        return repository.countAllByUserGroupedBySpecificStatus(user,status);
    }

    @Override
    public boolean delete(Integer id) {
        return repository.delete(id);
    }

    @Override
    public UserGameStatusItem update(Integer id, float userRating, String annotation, User user, Game game, Status status) {
        UserGameStatusItem item = new UserGameStatusItem(id);
        item.setUserRating(userRating);
        item.setAnnotation(annotation);
        item.setUser(user);
        item.setGame(game);
        item.setStatus(status);
        return repository.update(item);
    }

    @Override
    public UserGameStatusItem updateRating(Integer id, float userRating) {
        UserGameStatusItem item = new UserGameStatusItem(id);
        item.setUserRating(userRating);

        return repository.updateRating(item);
    }

    @Override
    public UserGameStatusItem updateAnnotation(Integer id, String annotation) {
        UserGameStatusItem item = new UserGameStatusItem(id);
        item.setAnnotation(annotation);

        return repository.updateAnnotation(item);    }

    @Override
    public UserGameStatusItem updateStatus(Integer id, Status status) {
        UserGameStatusItem item = new UserGameStatusItem(id);
        item.setStatus(status);

        return repository.updateStatus(item);
    }
}
